const { WIDTH, HEIGHT, HUD_HEIGHT, ROUND_MS, HIGH_SCORE_KEY, Target, Game } = require('../js/main.js');

function createMockCanvas() {
  const ctx = {
    save: jest.fn(),
    restore: jest.fn(),
    scale: jest.fn(),
    clearRect: jest.fn(),
    fillRect: jest.fn(),
    beginPath: jest.fn(),
    arc: jest.fn(),
    fill: jest.fn(),
    stroke: jest.fn(),
    moveTo: jest.fn(),
    lineTo: jest.fn(),
    arcTo: jest.fn(),
    closePath: jest.fn(),
    translate: jest.fn(),
    rotate: jest.fn(),
    fillText: jest.fn(),
  };
  return {
    ctx,
    width: 0,
    height: 0,
    getContext: jest.fn(() => ctx),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    getBoundingClientRect: jest.fn(() => ({ left: 0, top: 0, width: WIDTH, height: HEIGHT })),
  };
}

function createGame() {
  return new Game(createMockCanvas());
}

beforeEach(() => {
  window.localStorage.clear();
  global.requestAnimationFrame = jest.fn();
});

describe('Target', () => {
  test('starts in the spawning state', () => {
    const t = new Target(100, 100, 40, 1000);
    expect(t.state).toBe('spawning');
    expect(t.isDone).toBe(false);
  });

  test('moves spawning -> alive -> expired -> done as it ages', () => {
    const t = new Target(100, 100, 40, 500);

    t.update(100);
    expect(t.state).toBe('spawning');

    t.update(100); // age 200 > 160
    expect(t.state).toBe('alive');

    t.update(300); // age 500 >= lifespan 500
    expect(t.state).toBe('expired');

    t.update(100); // resolveAnim 100, not yet done
    expect(t.isDone).toBe(false);

    t.update(150); // resolveAnim 250 > 220
    expect(t.isDone).toBe(true);
  });

  test('a hit target also resolves to done after its animation', () => {
    const t = new Target(100, 100, 40, 500);
    t.update(200);
    t.state = 'hit';
    t.update(221);
    expect(t.isDone).toBe(true);
  });

  test('containsPoint respects the radius', () => {
    const t = new Target(500, 400, 30, 1000);
    expect(t.containsPoint(500, 400)).toBe(true);
    expect(t.containsPoint(520, 400)).toBe(true); // 20 <= 30
    expect(t.containsPoint(540, 400)).toBe(false); // 40 > 30
  });

  test('scoreFor peaks at the center and decays to the edge', () => {
    const t = new Target(0, 0, 50, 1000);
    expect(t.scoreFor(0, 0)).toBe(100);
    expect(t.scoreFor(50, 0)).toBe(5); // exactly on the edge -> minimum score
    expect(t.scoreFor(100, 0)).toBe(0); // outside the target entirely

    const near = t.scoreFor(10, 0);
    const far = t.scoreFor(40, 0);
    expect(near).toBeGreaterThan(far);
    expect(far).toBeGreaterThanOrEqual(5);
  });
});

describe('Game state machine', () => {
  test('boots into the menu state with a full clock', () => {
    const g = createGame();
    expect(g.state).toBe('menu');
    expect(g.timeLeft).toBe(ROUND_MS);
    expect(g.score).toBe(0);
  });

  test('startIntro resets round stats and enters the intro state', () => {
    const g = createGame();
    g.score = 999;
    g.combo = 5;
    g.startIntro();
    expect(g.state).toBe('intro');
    expect(g.score).toBe(0);
    expect(g.combo).toBe(0);
    expect(g.timeLeft).toBe(ROUND_MS);
  });

  test('Escape pauses while playing and resumes from paused', () => {
    const g = createGame();
    g.state = 'playing';
    g.onKeyDown({ key: 'Escape' });
    expect(g.state).toBe('paused');
    g.onKeyDown({ key: 'Escape' });
    expect(g.state).toBe('playing');
  });

  test('R restarts from the gameover screen, Enter starts from the menu', () => {
    const g = createGame();
    g.state = 'gameover';
    g.onKeyDown({ key: 'r' });
    expect(g.state).toBe('intro');

    const g2 = createGame();
    g2.onKeyDown({ key: 'Enter' });
    expect(g2.state).toBe('intro');
  });

  test('intro counts down 3-2-1-GO before play starts', () => {
    const g = createGame();
    g.startIntro();
    for (let i = 0; i < 4; i++) {
      expect(g.state).toBe('intro');
      g.update(700);
    }
    expect(g.state).toBe('playing');
    expect(g.target).not.toBeNull();
  });
});

describe('scoring and combo', () => {
  test('a hit inside the target increases score, combo and totalHits', () => {
    const g = createGame();
    g.state = 'playing';
    g.target = new Target(400, 300, 50, 1000);
    g.target.state = 'alive';

    g.handleShot(400, 300); // dead center -> 100 points, combo 1 -> x1.0 multiplier

    expect(g.score).toBe(100);
    expect(g.combo).toBe(1);
    expect(g.totalHits).toBe(1);
    expect(g.totalShots).toBe(1);
    expect(g.target.state).toBe('hit');
  });

  test('combo raises the score multiplier on consecutive hits', () => {
    const g = createGame();
    g.state = 'playing';
    g.combo = 4; // next hit is the 5th consecutive hit -> +32% multiplier

    g.target = new Target(200, 200, 50, 1000);
    g.target.state = 'alive';
    g.handleShot(200, 200); // bullseye: 100 base points

    expect(g.combo).toBe(5);
    expect(g.score).toBe(Math.round(100 * (1 + 4 * 0.08)));
  });

  test('missing the target resets combo without scoring', () => {
    const g = createGame();
    g.state = 'playing';
    g.combo = 3;
    g.target = new Target(200, 200, 30, 1000);
    g.target.state = 'alive';

    g.handleShot(900, 700); // far outside the target

    expect(g.combo).toBe(0);
    expect(g.score).toBe(0);
    expect(g.totalShots).toBe(1);
    expect(g.totalHits).toBe(0);
    expect(g.target.state).toBe('alive'); // target survives a miss
  });

  test('a target expiring while alive resets the combo', () => {
    const g = createGame();
    g.state = 'playing';
    g.combo = 3;
    g.target = new Target(200, 200, 30, 100);
    g.target.state = 'alive';
    g.target.age = 100; // will flip to expired on the next update

    g.update(16);

    expect(g.combo).toBe(0);
  });
});

describe('post-round statistics', () => {
  test('accuracy and average hit score are derived from shots/hits', () => {
    const g = createGame();
    g.totalShots = 4;
    g.totalHits = 3;
    g.hitScoreSum = 240; // avg 80

    expect(g.accuracy).toBe(75);
    expect(g.avgHitScore).toBe(80);
  });

  test('accuracy and average default to 0 with no shots fired', () => {
    const g = createGame();
    expect(g.accuracy).toBe(0);
    expect(g.avgHitScore).toBe(0);
  });

  test.each([
    [90, 80, 'EXCELLENT'],
    [65, 60, 'GOOD'],
    [45, 40, 'FAIR'],
    [10, 10, 'KEEP PRACTICING'],
  ])('rating for accuracy %i%% / avg %i -> %s', (accuracyPct, avg, label) => {
    const g = createGame();
    g.totalShots = 100;
    g.totalHits = accuracyPct;
    g.hitScoreSum = avg * accuracyPct;
    expect(g.rating.label).toBe(label);
  });

  test('finishRound persists a new best score to localStorage', () => {
    const g = createGame();
    g.score = 555;
    g.highScore = 100;

    g.finishRound();

    expect(g.state).toBe('gameover');
    expect(g.isNewBest).toBe(true);
    expect(g.highScore).toBe(555);
    expect(window.localStorage.getItem(HIGH_SCORE_KEY)).toBe('555');
  });

  test('finishRound does not overwrite a higher existing best score', () => {
    const g = createGame();
    g.score = 50;
    g.highScore = 200;

    g.finishRound();

    expect(g.isNewBest).toBe(false);
    expect(g.highScore).toBe(200);
    expect(window.localStorage.getItem(HIGH_SCORE_KEY)).toBeNull();
  });
});

describe('difficulty ramp', () => {
  test('targets start larger and longer-lived than they end up', () => {
    const g = createGame();

    g.elapsed = 0;
    g.spawnTarget();
    const early = g.target;

    g.elapsed = ROUND_MS;
    g.spawnTarget();
    const late = g.target;

    expect(early.radius).toBeGreaterThan(late.radius);
    expect(early.lifespan).toBeGreaterThan(late.lifespan);
  });

  test('spawned targets always stay within the play area, below the HUD', () => {
    const g = createGame();
    for (let i = 0; i < 20; i++) {
      g.elapsed = Math.random() * ROUND_MS;
      g.spawnTarget();
      const { x, y, radius } = g.target;
      expect(x - radius).toBeGreaterThanOrEqual(0);
      expect(x + radius).toBeLessThanOrEqual(WIDTH);
      expect(y - radius).toBeGreaterThanOrEqual(HUD_HEIGHT);
      expect(y + radius).toBeLessThanOrEqual(HEIGHT);
    }
  });
});
