class TetrisGame {
    constructor() {
        this.ROWS = 20;
        this.COLS = 10;
        this.CELL_SIZE = 30;
        
        // Game state
        this.board = [];
        this.currentPiece = null;
        this.nextPiece = null;
        this.score = 0;
        this.lines = 0;
        this.level = 1;
        this.gameRunning = false;
        this.gamePaused = false;
        this.dropSpeed = 800;
        
        // DOM elements
        this.gameBoard = document.getElementById('gameBoard');
        this.scoreDisplay = document.getElementById('score');
        this.levelDisplay = document.getElementById('level');
        this.linesDisplay = document.getElementById('lines');
        this.nextPieceDisplay = document.getElementById('nextPiece');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.gameOverModal = document.getElementById('gameOverModal');
        this.restartBtn = document.getElementById('restartBtn');
        this.finalScore = document.getElementById('finalScore');
        
        // Event listeners
        this.startBtn.addEventListener('click', () => this.startGame());
        this.pauseBtn.addEventListener('click', () => this.togglePause());
        this.restartBtn.addEventListener('click', () => this.restart());
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // Tetromino shapes
        this.tetrominoes = {
            I: { shape: [[1,1,1,1]], color: 'i-piece' },
            O: { shape: [[1,1], [1,1]], color: 'o-piece' },
            T: { shape: [[0,1,0], [1,1,1]], color: 't-piece' },
            S: { shape: [[0,1,1], [1,1,0]], color: 's-piece' },
            Z: { shape: [[1,1,0], [0,1,1]], color: 'z-piece' },
            J: { shape: [[1,0,0], [1,1,1]], color: 'j-piece' },
            L: { shape: [[0,0,1], [1,1,1]], color: 'l-piece' }
        };
        
        this.init();
    }
    
    init() {
        // Initialize board
        for (let row = 0; row < this.ROWS; row++) {
            this.board[row] = [];
            for (let col = 0; col < this.COLS; col++) {
                this.board[row][col] = null;
            }
        }
        
        // Create DOM cells
        this.gameBoard.innerHTML = '';
        for (let i = 0; i < this.ROWS * this.COLS; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.id = `cell-${i}`;
            this.gameBoard.appendChild(cell);
        }
        
        this.nextPiece = this.generatePiece();
        this.updateDisplay();
    }
    
    generatePiece() {
        const keys = Object.keys(this.tetrominoes);
        const randomKey = keys[Math.floor(Math.random() * keys.length)];
        return {
            type: randomKey,
            shape: JSON.parse(JSON.stringify(this.tetrominoes[randomKey].shape)),
            color: this.tetrominoes[randomKey].color,
            row: 0,
            col: 3
        };
    }
    
    startGame() {
        if (this.gameRunning) return;
        this.gameRunning = true;
        this.gamePaused = false;
        this.currentPiece = this.nextPiece;
        this.nextPiece = this.generatePiece();
        this.gameOverModal.classList.add('hidden');
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        this.updateDisplay();
        this.gameLoop();
    }
    
    togglePause() {
        if (!this.gameRunning) return;
        this.gamePaused = !this.gamePaused;
        this.pauseBtn.textContent = this.gamePaused ? 'Resume' : 'Pause';
        if (!this.gamePaused) {
            this.gameLoop();
        }
    }
    
    gameLoop() {
        if (!this.gameRunning || this.gamePaused) return;
        
        if (!this.canMovePiece(this.currentPiece, 1, 0)) {
            this.lockPiece();
            this.clearLines();
            this.currentPiece = this.nextPiece;
            this.nextPiece = this.generatePiece();
            
            if (!this.canMovePiece(this.currentPiece, 0, 0)) {
                this.endGame();
                return;
            }
        } else {
            this.currentPiece.row++;
        }
        
        this.updateDisplay();
        setTimeout(() => this.gameLoop(), this.dropSpeed);
    }
    
    handleKeyPress(e) {
        if (!this.gameRunning || this.gamePaused) return;
        
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                if (this.canMovePiece(this.currentPiece, 0, -1)) {
                    this.currentPiece.col--;
                    this.updateDisplay();
                }
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (this.canMovePiece(this.currentPiece, 0, 1)) {
                    this.currentPiece.col++;
                    this.updateDisplay();
                }
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.rotatePiece();
                break;
            case 'ArrowDown':
                e.preventDefault();
                if (this.canMovePiece(this.currentPiece, 1, 0)) {
                    this.currentPiece.row++;
                    this.score += 1;
                    this.updateDisplay();
                }
                break;
        }
    }
    
    rotatePiece() {
        const originalShape = JSON.parse(JSON.stringify(this.currentPiece.shape));
        
        // Rotate: transpose and reverse each row
        const rotated = [];
        for (let col = 0; col < originalShape[0].length; col++) {
            const row = [];
            for (let r = originalShape.length - 1; r >= 0; r--) {
                row.push(originalShape[r][col]);
            }
            rotated.push(row);
        }
        
        this.currentPiece.shape = rotated;
        
        if (!this.canMovePiece(this.currentPiece, 0, 0)) {
            // If rotation causes collision, revert
            this.currentPiece.shape = originalShape;
        }
        
        this.updateDisplay();
    }
    
    canMovePiece(piece, rowDelta, colDelta) {
        const newRow = piece.row + rowDelta;
        const newCol = piece.col + colDelta;
        
        for (let r = 0; r < piece.shape.length; r++) {
            for (let c = 0; c < piece.shape[r].length; c++) {
                if (piece.shape[r][c]) {
                    const boardRow = newRow + r;
                    const boardCol = newCol + c;
                    
                    // Check boundaries
                    if (boardRow < 0 || boardRow >= this.ROWS || 
                        boardCol < 0 || boardCol >= this.COLS) {
                        return false;
                    }
                    
                    // Check collision with placed pieces
                    if (this.board[boardRow][boardCol] !== null) {
                        return false;
                    }
                }
            }
        }
        
        return true;
    }
    
    lockPiece() {
        for (let r = 0; r < this.currentPiece.shape.length; r++) {
            for (let c = 0; c < this.currentPiece.shape[r].length; c++) {
                if (this.currentPiece.shape[r][c]) {
                    const boardRow = this.currentPiece.row + r;
                    const boardCol = this.currentPiece.col + c;
                    
                    if (boardRow >= 0) {
                        this.board[boardRow][boardCol] = this.currentPiece.color;
                    }
                }
            }
        }
    }
    
    clearLines() {
        let linesCleared = 0;
        
        for (let row = this.ROWS - 1; row >= 0; row--) {
            let isFull = true;
            for (let col = 0; col < this.COLS; col++) {
                if (this.board[row][col] === null) {
                    isFull = false;
                    break;
                }
            }
            
            if (isFull) {
                this.board.splice(row, 1);
                this.board.unshift(Array(this.COLS).fill(null));
                linesCleared++;
                row++; // Check this row again
            }
        }
        
        if (linesCleared > 0) {
            this.lines += linesCleared;
            
            // Calculate score based on lines cleared at once
            const scores = [0, 40, 100, 300, 1200];
            this.score += scores[Math.min(linesCleared, 4)] * this.level;
            
            // Update level every 10 lines
            this.level = Math.floor(this.lines / 10) + 1;
            this.dropSpeed = Math.max(100, 800 - (this.level - 1) * 50);
        }
    }
    
    endGame() {
        this.gameRunning = false;
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
        this.pauseBtn.textContent = 'Pause';
        this.finalScore.textContent = this.score;
        this.gameOverModal.classList.remove('hidden');
    }
    
    restart() {
        this.score = 0;
        this.lines = 0;
        this.level = 1;
        this.dropSpeed = 800;
        this.gameRunning = false;
        this.gamePaused = false;
        this.init();
    }
    
    updateDisplay() {
        // Update board display
        for (let row = 0; row < this.ROWS; row++) {
            for (let col = 0; col < this.COLS; col++) {
                const cellId = `cell-${row * this.COLS + col}`;
                const cell = document.getElementById(cellId);
                
                if (this.board[row][col]) {
                    cell.className = `cell filled ${this.board[row][col]}`;
                } else {
                    cell.className = 'cell';
                }
            }
        }
        
        // Draw current piece
        if (this.currentPiece) {
            for (let r = 0; r < this.currentPiece.shape.length; r++) {
                for (let c = 0; c < this.currentPiece.shape[r].length; c++) {
                    if (this.currentPiece.shape[r][c]) {
                        const boardRow = this.currentPiece.row + r;
                        const boardCol = this.currentPiece.col + c;
                        
                        if (boardRow >= 0 && boardRow < this.ROWS && 
                            boardCol >= 0 && boardCol < this.COLS) {
                            const cellId = `cell-${boardRow * this.COLS + boardCol}`;
                            const cell = document.getElementById(cellId);
                            cell.className = `cell filled ${this.currentPiece.color}`;
                        }
                    }
                }
            }
        }
        
        // Update stats
        this.scoreDisplay.textContent = this.score;
        this.levelDisplay.textContent = this.level;
        this.linesDisplay.textContent = this.lines;
        
        // Update next piece display
        this.updateNextPieceDisplay();
    }
    
    updateNextPieceDisplay() {
        this.nextPieceDisplay.innerHTML = '';
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                
                if (this.nextPiece && i < this.nextPiece.shape.length && 
                    j < this.nextPiece.shape[i].length && this.nextPiece.shape[i][j]) {
                    cell.classList.add('filled', this.nextPiece.color);
                }
                
                this.nextPieceDisplay.appendChild(cell);
            }
        }
    }
}

// Start the game when page loads
window.addEventListener('DOMContentLoaded', () => {
    new TetrisGame();
});
