export type GameState = 'menu' | 'playing' | 'paused' | 'gameOver';

export type BulletType = 'player' | 'enemy';

export interface GameObject {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
}

export interface KeyState {
  [key: string]: boolean;
}