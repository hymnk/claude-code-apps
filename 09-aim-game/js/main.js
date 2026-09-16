'use strict';

/* =========================================================================
   AIM FORGE — a mouse-aim precision trainer
   Solarized-light, flat "stylish" aesthetic. Pure Canvas2D, no dependencies.
   ========================================================================= */

const WIDTH = 1024;
const HEIGHT = 768;
const HUD_HEIGHT = 68;
const ROUND_MS = 60000;
const HIGH_SCORE_KEY = 'aimForge.highScore';

const COLORS = {
  base3: '#fdf6e3',
  base2: '#eee8d5',
  base1: '#93a1a1',
  base0: '#839496',
  base00: '#657b83',
  base01: '#586e75',
  base02: '#073642',
  yellow: '#b58900',
  orange: '#cb4b16',
  red: '#dc322f',
  magenta: '#d33682',
  violet: '#6c71c4',
  blue: '#268bd2',
  cyan: '#2aa198',
  green: '#859900',
};

// ---------------------------------------------------------------- utils --

const rand = (min, max) => min + Math.random() * (max - min);
const randInt = (min, max) => Math.floor(rand(min, max + 1));
const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
const lerp = (a, b, t) => a + (b - a) * clamp(t, 0, 1);
const dist = (x1, y1, x2, y2) => Math.hypot(x2 - x1, y2 - y1);

function easeOutBack(t) {
  const c1 = 1.70158;
  const c3 = c1 + 1;
  const x = clamp(t, 0, 1);
  return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
}

function easeOutCubic(t) {
  const x = clamp(t, 0, 1);
  return 1 - Math.pow(1 - x, 3);
}

function hexToRgba(hex, alpha) {
  const v = hex.replace('#', '');
  const r = parseInt(v.substring(0, 2), 16);
  const g = parseInt(v.substring(2, 4), 16);
  const b = parseInt(v.substring(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

// --------------------------------------------------------------- target --

const TARGET_ACCENTS = [COLORS.blue, COLORS.cyan, COLORS.violet, COLORS.magenta];

class Target {
  constructor(x, y, radius, lifespan) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.lifespan = lifespan;
    this.age = 0;
    this.state = 'spawning'; // spawning | alive | hit | expired | done
    this.resolveAnim = 0;
    this.accent = TARGET_ACCENTS[randInt(0, TARGET_ACCENTS.length - 1)];
  }

  update(dt) {
    this.age += dt;
    if (this.state === 'spawning') {
      if (this.age > 160) this.state = 'alive';
    } else if (this.state === 'alive') {
      if (this.age >= this.lifespan) this.state = 'expired';
    } else if (this.state === 'hit' || this.state === 'expired') {
      this.resolveAnim += dt;
      if (this.resolveAnim > 220) this.state = 'done';
    }
  }

  get isDone() {
    return this.state === 'done';
  }

  get lifeProgress() {
    return clamp(this.age / this.lifespan, 0, 1);
  }

  get displayRadius() {
    if (this.state === 'spawning') {
      return this.radius * easeOutBack(this.age / 160);
    }
    if (this.state === 'hit') {
      return this.radius * (1 - easeOutCubic(this.resolveAnim / 220)) * 1.15;
    }
    if (this.state === 'expired') {
      return this.radius * (1 - 0.25 * easeOutCubic(this.resolveAnim / 220));
    }
    return this.radius;
  }

  get displayAlpha() {
    if (this.state === 'hit' || this.state === 'expired') {
      return 1 - easeOutCubic(this.resolveAnim / 220);
    }
    return 1;
  }

  containsPoint(px, py) {
    return dist(px, py, this.x, this.y) <= this.radius;
  }

  scoreFor(px, py) {
    const d = dist(px, py, this.x, this.y);
    if (d > this.radius) return 0;
    const t = 1 - d / this.radius;
    return Math.max(5, Math.round(100 * Math.pow(t, 1.4)));
  }

  draw(ctx) {
    const r = this.displayRadius;
    if (r <= 0.5) return;
    const alpha = this.displayAlpha;

    ctx.save();
    ctx.globalAlpha = alpha;

    // soft drop shadow
    ctx.beginPath();
    ctx.arc(this.x, this.y + 3, r, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(7, 54, 66, 0.12)';
    ctx.fill();

    // outer ring
    ctx.beginPath();
    ctx.arc(this.x, this.y, r, 0, Math.PI * 2);
    ctx.fillStyle = hexToRgba(this.accent, 0.16);
    ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = this.accent;
    ctx.stroke();

    // mid ring
    ctx.beginPath();
    ctx.arc(this.x, this.y, r * 0.62, 0, Math.PI * 2);
    ctx.fillStyle = hexToRgba(this.accent, 0.32);
    ctx.fill();

    // core
    ctx.beginPath();
    ctx.arc(this.x, this.y, r * 0.26, 0, Math.PI * 2);
    ctx.fillStyle = COLORS.base3;
    ctx.fill();
    ctx.beginPath();
    ctx.arc(this.x, this.y, r * 0.14, 0, Math.PI * 2);
    ctx.fillStyle = this.accent;
    ctx.fill();

    // lifespan sweep (remaining time)
    if (this.state === 'alive') {
      const remaining = 1 - this.lifeProgress;
      ctx.beginPath();
      ctx.arc(this.x, this.y, r + 6, -Math.PI / 2, -Math.PI / 2 + remaining * Math.PI * 2);
      ctx.lineWidth = 3;
      ctx.strokeStyle = remaining < 0.3 ? COLORS.red : hexToRgba(COLORS.base01, 0.55);
      ctx.lineCap = 'round';
      ctx.stroke();
    }

    ctx.restore();
  }
}

// -------------------------------------------------------------- particle --

class Particle {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    const angle = rand(0, Math.PI * 2);
    const speed = rand(90, 260);
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed;
    this.size = rand(3, 7);
    this.rotation = rand(0, Math.PI * 2);
    this.spin = rand(-4, 4);
    this.color = color;
    this.age = 0;
    this.life = rand(350, 550);
  }

  update(dt) {
    const s = dt / 1000;
    this.x += this.vx * s;
    this.y += this.vy * s;
    this.vy += 420 * s;
    this.vx *= 1 - 1.6 * s;
    this.rotation += this.spin * s;
    this.age += dt;
  }

  get done() {
    return this.age >= this.life;
  }

  draw(ctx) {
    const alpha = 1 - this.age / this.life;
    if (alpha <= 0) return;
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation);
    ctx.fillStyle = this.color;
    const s = this.size * alpha;
    ctx.fillRect(-s / 2, -s / 2, s, s);
    ctx.restore();
  }
}

// ---------------------------------------------------------- floating text --

class FloatingText {
  constructor(x, y, text, color, big) {
    this.x = x;
    this.y = y;
    this.text = text;
    this.color = color;
    this.big = big;
    this.age = 0;
    this.life = 650;
  }

  update(dt) {
    this.age += dt;
  }

  get done() {
    return this.age >= this.life;
  }

  draw(ctx) {
    const t = this.age / this.life;
    const alpha = 1 - easeOutCubic(t);
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.fillStyle = this.color;
    ctx.font = `${this.big ? 700 : 600} ${this.big ? 26 : 18}px -apple-system, "Segoe UI", sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(this.text, this.x, this.y - easeOutCubic(t) * 46);
    ctx.restore();
  }
}

// -------------------------------------------------------------- button ---

class Button {
  constructor(x, y, w, h, label, accent) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.label = label;
    this.accent = accent || COLORS.blue;
  }

  hitTest(px, py) {
    return px >= this.x && px <= this.x + this.w && py >= this.y && py <= this.y + this.h;
  }

  draw(ctx, hovered) {
    ctx.save();
    roundRect(ctx, this.x, this.y, this.w, this.h, this.h / 2);
    ctx.fillStyle = hovered ? this.accent : hexToRgba(this.accent, 0.92);
    ctx.fill();
    if (hovered) {
      ctx.lineWidth = 2;
      ctx.strokeStyle = hexToRgba(COLORS.base02, 0.25);
      ctx.stroke();
    }
    ctx.fillStyle = COLORS.base3;
    ctx.font = '700 20px -apple-system, "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(this.label, this.x + this.w / 2, this.y + this.h / 2 + 1);
    ctx.restore();
  }
}

// ----------------------------------------------------------------- game --

class Game {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.dpr = window.devicePixelRatio || 1;
    canvas.width = WIDTH * this.dpr;
    canvas.height = HEIGHT * this.dpr;
    this.ctx.scale(this.dpr, this.dpr);

    this.state = 'menu'; // menu | intro | playing | paused | gameover
    this.mouse = { x: WIDTH / 2, y: HEIGHT / 2 };
    this.shake = 0;
    this.flash = null; // { color, age, life }
    this.highScore = Number(localStorage.getItem(HIGH_SCORE_KEY) || 0);

    this.playBtn = new Button(WIDTH / 2 - 100, 480, 200, 56, 'PLAY', COLORS.blue);
    this.retryBtn = new Button(WIDTH / 2 - 110, 560, 220, 54, 'RETRY (R)', COLORS.blue);
    this.menuBtn = new Button(WIDTH / 2 - 110, 626, 220, 46, 'MENU (ESC)', COLORS.base1);
    this.resumeBtn = new Button(WIDTH / 2 - 100, 380, 200, 54, 'RESUME', COLORS.green);

    this.resetRound();

    canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
    canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
    window.addEventListener('keydown', (e) => this.onKeyDown(e));

    this.lastTime = performance.now();
    requestAnimationFrame((t) => this.loop(t));
  }

  resetRound() {
    this.score = 0;
    this.combo = 0;
    this.maxCombo = 0;
    this.totalShots = 0;
    this.totalHits = 0;
    this.hitScoreSum = 0;
    this.timeLeft = ROUND_MS;
    this.elapsed = 0;
    this.target = null;
    this.particles = [];
    this.floaters = [];
    this.introValue = 3;
    this.introTimer = 0;
  }

  // -------------------------------------------------------------- input --

  toCanvasCoords(e) {
    const rect = this.canvas.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * WIDTH;
    const y = ((e.clientY - rect.top) / rect.height) * HEIGHT;
    return { x, y };
  }

  onMouseMove(e) {
    this.mouse = this.toCanvasCoords(e);
  }

  onMouseDown(e) {
    const { x, y } = this.toCanvasCoords(e);
    if (this.state === 'menu') {
      if (this.playBtn.hitTest(x, y)) this.startIntro();
    } else if (this.state === 'playing') {
      this.handleShot(x, y);
    } else if (this.state === 'paused') {
      if (this.resumeBtn.hitTest(x, y)) this.state = 'playing';
    } else if (this.state === 'gameover') {
      if (this.retryBtn.hitTest(x, y)) this.startIntro();
      else if (this.menuBtn.hitTest(x, y)) this.state = 'menu';
    }
  }

  onKeyDown(e) {
    if (e.key === 'Escape') {
      if (this.state === 'playing') this.state = 'paused';
      else if (this.state === 'paused') this.state = 'playing';
      else if (this.state === 'gameover') this.state = 'menu';
    } else if ((e.key === 'r' || e.key === 'R') && this.state === 'gameover') {
      this.startIntro();
    } else if (e.key === 'Enter' && this.state === 'menu') {
      this.startIntro();
    }
  }

  startIntro() {
    this.resetRound();
    this.state = 'intro';
  }

  spawnTarget() {
    const f = this.elapsed / ROUND_MS;
    const radius = lerp(48, 27, f) + rand(-4, 4);
    const lifespan = lerp(1450, 780, f) + rand(-80, 80);
    const margin = radius + 10;
    const x = rand(margin, WIDTH - margin);
    const y = rand(HUD_HEIGHT + margin, HEIGHT - margin);
    this.target = new Target(x, y, radius, lifespan);
  }

  handleShot(x, y) {
    if (!this.target || this.target.state !== 'alive') return;
    this.totalShots++;

    if (this.target.containsPoint(x, y)) {
      const points = this.target.scoreFor(x, y);
      this.combo++;
      this.maxCombo = Math.max(this.maxCombo, this.combo);
      const multiplier = 1 + Math.min(this.combo - 1, 9) * 0.08;
      const gained = Math.round(points * multiplier);
      this.score += gained;
      this.totalHits++;
      this.hitScoreSum += points;

      this.target.state = 'hit';
      this.spawnBurst(this.target.x, this.target.y, this.target.accent);
      const big = points >= 92;
      this.floaters.push(new FloatingText(x, y - 10, `+${gained}${big ? ' !' : ''}`, big ? COLORS.orange : COLORS.base01, big));
      if (this.combo > 1 && this.combo % 5 === 0) {
        this.floaters.push(new FloatingText(x, y - 40, `COMBO x${this.combo}`, COLORS.violet, true));
      }
      this.flash = { color: COLORS.green, age: 0, life: 160 };
    } else {
      this.combo = 0;
      this.shake = 8;
      this.flash = { color: COLORS.red, age: 0, life: 220 };
    }
  }

  spawnBurst(x, y, color) {
    const n = 16;
    for (let i = 0; i < n; i++) {
      this.particles.push(new Particle(x, y, Math.random() < 0.5 ? color : COLORS.base01));
    }
  }

  // ------------------------------------------------------------- update --

  update(dt) {
    if (this.state === 'intro') {
      this.introTimer += dt;
      if (this.introTimer >= 700) {
        this.introTimer = 0;
        this.introValue--;
        if (this.introValue < 0) {
          this.state = 'playing';
          this.spawnTarget();
        }
      }
    } else if (this.state === 'playing') {
      this.elapsed += dt;
      this.timeLeft = Math.max(0, ROUND_MS - this.elapsed);

      if (this.target) {
        const wasAlive = this.target.state === 'alive';
        this.target.update(dt);
        if (wasAlive && this.target.state === 'expired') {
          this.combo = 0;
        }
        if (this.target.isDone) {
          this.target = null;
        }
      }
      if (!this.target && this.timeLeft > 0) {
        this.spawnTarget();
      }
      if (this.timeLeft <= 0) {
        this.finishRound();
      }
    }

    this.particles.forEach((p) => p.update(dt));
    this.particles = this.particles.filter((p) => !p.done);
    this.floaters.forEach((f) => f.update(dt));
    this.floaters = this.floaters.filter((f) => !f.done);

    if (this.shake > 0) this.shake = Math.max(0, this.shake - dt * 0.05);
    if (this.flash) {
      this.flash.age += dt;
      if (this.flash.age >= this.flash.life) this.flash = null;
    }
  }

  finishRound() {
    this.state = 'gameover';
    if (this.score > this.highScore) {
      this.highScore = this.score;
      localStorage.setItem(HIGH_SCORE_KEY, String(this.highScore));
      this.isNewBest = true;
    } else {
      this.isNewBest = false;
    }
  }

  get accuracy() {
    return this.totalShots === 0 ? 0 : Math.round((this.totalHits / this.totalShots) * 100);
  }

  get avgHitScore() {
    return this.totalHits === 0 ? 0 : Math.round(this.hitScoreSum / this.totalHits);
  }

  get rating() {
    const acc = this.accuracy;
    const avg = this.avgHitScore;
    if (acc >= 80 && avg >= 75) return { label: 'EXCELLENT', color: COLORS.green };
    if (acc >= 60 && avg >= 55) return { label: 'GOOD', color: COLORS.blue };
    if (acc >= 40 && avg >= 35) return { label: 'FAIR', color: COLORS.yellow };
    return { label: 'KEEP PRACTICING', color: COLORS.orange };
  }

  // ------------------------------------------------------------- render --

  loop(now) {
    const dt = Math.min(50, now - this.lastTime);
    this.lastTime = now;
    this.update(dt);
    this.render();
    requestAnimationFrame((t) => this.loop(t));
  }

  render() {
    const ctx = this.ctx;
    ctx.save();
    ctx.clearRect(0, 0, WIDTH, HEIGHT);

    const shakeX = this.shake ? rand(-this.shake, this.shake) : 0;
    const shakeY = this.shake ? rand(-this.shake, this.shake) : 0;
    ctx.translate(shakeX, shakeY);

    this.drawBackground(ctx);

    if (this.state === 'menu') {
      this.drawMenu(ctx);
    } else if (this.state === 'intro') {
      this.drawHUD(ctx);
      this.drawIntro(ctx);
    } else if (this.state === 'playing' || this.state === 'paused') {
      if (this.target) this.target.draw(ctx);
      this.particles.forEach((p) => p.draw(ctx));
      this.floaters.forEach((f) => f.draw(ctx));
      this.drawHUD(ctx);
      if (this.state === 'paused') this.drawPaused(ctx);
    } else if (this.state === 'gameover') {
      this.drawHUD(ctx);
      this.drawGameOver(ctx);
    }

    if (this.flash) {
      const a = (1 - this.flash.age / this.flash.life) * 0.12;
      ctx.fillStyle = hexToRgba(this.flash.color, a);
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
    }

    if (this.state !== 'menu') this.drawCrosshair(ctx);
    ctx.restore();
  }

  drawBackground(ctx) {
    ctx.fillStyle = COLORS.base3;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    ctx.fillStyle = COLORS.base2;
    const step = 32;
    for (let x = step; x < WIDTH; x += step) {
      for (let y = step; y < HEIGHT; y += step) {
        ctx.beginPath();
        ctx.arc(x, y, 1.4, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  drawCrosshair(ctx) {
    const { x, y } = this.mouse;
    const color = this.flash ? this.flash.color : COLORS.base01;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, 14, 0, Math.PI * 2);
    ctx.stroke();
    const gap = 6;
    const len = 8;
    [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dx, dy]) => {
      ctx.beginPath();
      ctx.moveTo(x + dx * (14 + gap), y + dy * (14 + gap));
      ctx.lineTo(x + dx * (14 + gap + len), y + dy * (14 + gap + len));
      ctx.stroke();
    });
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  drawHUD(ctx) {
    ctx.save();
    ctx.fillStyle = COLORS.base2;
    ctx.fillRect(0, 0, WIDTH, HUD_HEIGHT);
    ctx.strokeStyle = hexToRgba(COLORS.base1, 0.5);
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, HUD_HEIGHT);
    ctx.lineTo(WIDTH, HUD_HEIGHT);
    ctx.stroke();

    ctx.textBaseline = 'middle';
    ctx.font = '700 15px -apple-system, "Segoe UI", sans-serif';
    ctx.fillStyle = COLORS.base01;

    ctx.textAlign = 'left';
    ctx.fillText(`SCORE  ${this.score}`, 24, HUD_HEIGHT / 2);

    ctx.textAlign = 'center';
    const totalSeconds = Math.ceil(this.timeLeft / 1000);
    const mm = Math.floor(totalSeconds / 60);
    const ss = totalSeconds % 60;
    ctx.fillStyle = totalSeconds <= 10 && this.state === 'playing' ? COLORS.red : COLORS.base01;
    ctx.fillText(`${mm}:${String(ss).padStart(2, '0')}`, WIDTH / 2, HUD_HEIGHT / 2 - 6);
    const barW = 160;
    const progress = this.state === 'menu' ? 1 : this.timeLeft / ROUND_MS;
    ctx.fillStyle = hexToRgba(COLORS.base1, 0.3);
    roundRect(ctx, WIDTH / 2 - barW / 2, HUD_HEIGHT / 2 + 10, barW, 4, 2);
    ctx.fill();
    ctx.fillStyle = COLORS.blue;
    roundRect(ctx, WIDTH / 2 - barW / 2, HUD_HEIGHT / 2 + 10, barW * progress, 4, 2);
    ctx.fill();

    ctx.textAlign = 'right';
    ctx.fillStyle = COLORS.base01;
    ctx.fillText(`COMBO x${this.combo}   ACC ${this.accuracy}%`, WIDTH - 24, HUD_HEIGHT / 2);
    ctx.restore();
  }

  drawMenu(ctx) {
    ctx.save();
    ctx.textAlign = 'center';

    ctx.fillStyle = COLORS.base01;
    ctx.font = '800 56px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText('AIM FORGE', WIDTH / 2, 220);

    ctx.fillStyle = COLORS.base00;
    ctx.font = '500 18px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText('マウスカーソルで的を狙い、60秒間の精密射撃スコアを競う', WIDTH / 2, 268);

    // decorative target
    const demo = new Target(WIDTH / 2, 370, 46, 999999);
    demo.state = 'alive';
    demo.age = 0;
    demo.draw(ctx);

    const hovered = this.playBtn.hitTest(this.mouse.x, this.mouse.y);
    this.playBtn.draw(ctx, hovered);

    ctx.fillStyle = COLORS.base00;
    ctx.font = '500 14px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText('中心に近いほど高得点 ・ コンボで倍率アップ ・ 制限時間内に的が消える前に撃て', WIDTH / 2, 560);

    if (this.highScore > 0) {
      ctx.fillStyle = COLORS.yellow;
      ctx.font = '700 16px -apple-system, "Segoe UI", sans-serif';
      ctx.fillText(`BEST SCORE  ${this.highScore}`, WIDTH / 2, 600);
    }
    ctx.restore();
  }

  drawIntro(ctx) {
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const t = this.introTimer / 700;
    const scale = 1 + (1 - easeOutCubic(t)) * 0.6;
    const alpha = 1 - t * 0.3;
    ctx.globalAlpha = clamp(alpha, 0, 1);
    ctx.translate(WIDTH / 2, HEIGHT / 2);
    ctx.scale(scale, scale);
    ctx.fillStyle = this.introValue <= 0 ? COLORS.green : COLORS.blue;
    ctx.font = '800 120px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText(this.introValue <= 0 ? 'GO' : String(this.introValue), 0, 0);
    ctx.restore();
  }

  drawPaused(ctx) {
    ctx.save();
    ctx.fillStyle = 'rgba(238, 232, 213, 0.85)';
    ctx.fillRect(0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT);
    ctx.textAlign = 'center';
    ctx.fillStyle = COLORS.base01;
    ctx.font = '800 40px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText('PAUSED', WIDTH / 2, 320);
    const hovered = this.resumeBtn.hitTest(this.mouse.x, this.mouse.y);
    this.resumeBtn.draw(ctx, hovered);
    ctx.restore();
  }

  drawGameOver(ctx) {
    ctx.save();
    ctx.textAlign = 'center';

    ctx.fillStyle = COLORS.base01;
    ctx.font = '800 40px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText('ROUND COMPLETE', WIDTH / 2, 150);

    if (this.isNewBest) {
      ctx.fillStyle = COLORS.orange;
      ctx.font = '700 16px -apple-system, "Segoe UI", sans-serif';
      ctx.fillText('★ NEW BEST SCORE ★', WIDTH / 2, 182);
    }

    ctx.fillStyle = COLORS.base02;
    ctx.font = '800 64px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText(String(this.score), WIDTH / 2, 250);

    const rating = this.rating;
    ctx.fillStyle = rating.color;
    ctx.font = '700 20px -apple-system, "Segoe UI", sans-serif';
    ctx.fillText(rating.label, WIDTH / 2, 288);

    const stats = [
      ['HITS', `${this.totalHits} / ${this.totalShots}`],
      ['ACCURACY', `${this.accuracy}%`],
      ['AVG HIT SCORE', `${this.avgHitScore}`],
      ['MAX COMBO', `x${this.maxCombo}`],
      ['BEST SCORE', `${this.highScore}`],
    ];
    ctx.font = '600 16px -apple-system, "Segoe UI", sans-serif';
    const startY = 330;
    stats.forEach(([label, value], i) => {
      const y = startY + i * 26;
      ctx.textAlign = 'left';
      ctx.fillStyle = COLORS.base00;
      ctx.fillText(label, WIDTH / 2 - 140, y);
      ctx.textAlign = 'right';
      ctx.fillStyle = COLORS.base01;
      ctx.fillText(value, WIDTH / 2 + 140, y);
    });

    const rHover = this.retryBtn.hitTest(this.mouse.x, this.mouse.y);
    const mHover = this.menuBtn.hitTest(this.mouse.x, this.mouse.y);
    this.retryBtn.draw(ctx, rHover);
    this.menuBtn.draw(ctx, mHover);
    ctx.restore();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('game');
  window.__game = new Game(canvas);
});
