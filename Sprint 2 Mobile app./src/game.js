// These functions contain the rules for 2048 and do not depend on the screen UI.

export function makeEmptyBoard(size) {
  return Array.from({ length: size }, () => Array(size).fill(0));
}

function copyBoard(board) {
  return board.map((row) => [...row]);
}

// Adds a random tile to an empty square using the selected spawn values.
export function addRandomTile(board, spawnValues) {
  const empty = [];
  board.forEach((row, r) => row.forEach((value, c) => {
    if (value === 0) empty.push([r, c]);
  }));
  if (!empty.length) return board;
  const [r, c] = empty[Math.floor(Math.random() * empty.length)];
  const value = spawnValues[Math.floor(Math.random() * spawnValues.length)];
  const next = copyBoard(board);
  next[r][c] = value;
  return next;
}

// Starts a fresh game with two tiles already on the board.
export function newGame(size, spawnValues) {
  let board = makeEmptyBoard(size);
  board = addRandomTile(board, spawnValues);
  board = addRandomTile(board, spawnValues);
  return { board, score: 0, won: false, over: false };
}

// Moves a row left, merging each matching pair only once.
function moveRowLeft(row) {
  const compacted = row.filter((value) => value !== 0);
  const result = [];
  let points = 0;
  for (let i = 0; i < compacted.length; i += 1) {
    if (compacted[i] === compacted[i + 1]) {
      const merged = compacted[i] * 2;
      result.push(merged);
      points += merged;
      i += 1;
    } else {
      result.push(compacted[i]);
    }
  }
  while (result.length < row.length) result.push(0);
  return { row: result, points };
}

// Rotating the board allows the same row-moving code to handle every direction.
function rotateClockwise(board) {
  const size = board.length;
  return Array.from({ length: size }, (_, r) =>
    Array.from({ length: size }, (_, c) => board[size - 1 - c][r])
  );
}

export function moveBoard(board, direction) {
  // Rotate so the requested direction becomes a left move.
  const turns = { left: 0, up: 3, right: 2, down: 1 }[direction];
  let rotated = copyBoard(board);
  for (let i = 0; i < turns; i += 1) rotated = rotateClockwise(rotated);

  let points = 0;
  let moved = rotated.map((row) => {
    const result = moveRowLeft(row);
    points += result.points;
    return result.row;
  });

  // Undo the rotation so the board faces the original direction again.
  for (let i = 0; i < (4 - turns) % 4; i += 1) moved = rotateClockwise(moved);
  return { board: moved, points };
}

// Returns false when the board is full and no neighboring tiles can merge.
export function hasMoves(board) {
  for (let r = 0; r < board.length; r += 1) {
    for (let c = 0; c < board.length; c += 1) {
      if (board[r][c] === 0) return true;
      if (c + 1 < board.length && board[r][c] === board[r][c + 1]) return true;
      if (r + 1 < board.length && board[r][c] === board[r + 1][c]) return true;
    }
  }
  return false;
}

// Applies a move and updates the score and game-over state.
export function playMove(game, direction, spawnValues) {
  const moved = moveBoard(game.board, direction);
  const changed = moved.board.some((row, r) =>
    row.some((value, c) => value !== game.board[r][c])
  );
  // A move against a wall should not create a new tile or change the score.
  if (!changed) return game;

  const board = addRandomTile(moved.board, spawnValues);
  const won = game.won || board.some((row) => row.some((value) => value >= 2048));
  return { board, score: game.score + moved.points, won, over: !hasMoves(board) };
}
