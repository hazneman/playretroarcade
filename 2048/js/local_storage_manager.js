window.fakeStorage = {
  _data: {},

  setItem: function (id, val) {
    return this._data[id] = String(val);
  },

  getItem: function (id) {
    return this._data.hasOwnProperty(id) ? this._data[id] : undefined;
  },

  removeItem: function (id) {
    return delete this._data[id];
  },

  clear: function () {
    return this._data = {};
  }
};

function LocalStorageManager() {
  // Namespaced: this site serves several games from one origin, and
  // A Dark Room also uses a bare "gameState" key.
  this.bestScoreKey     = "2048.bestScore";
  this.gameStateKey     = "2048.gameState";
  // one-time migration of the old un-namespaced best score
  try {
    var oldBest = window.localStorage.getItem("bestScore");
    if (oldBest !== null && window.localStorage.getItem(this.bestScoreKey) === null) {
      window.localStorage.setItem(this.bestScoreKey, oldBest);
      window.localStorage.removeItem("bestScore");
    }
    // clean up a stale un-namespaced 2048 save, but only if it is
    // unmistakably 2048's shape (A Dark Room uses the same key name)
    var oldState = window.localStorage.getItem("gameState");
    if (oldState) {
      var parsed = JSON.parse(oldState);
      if (parsed && parsed.grid && parsed.grid.cells && parsed.score !== undefined) {
        window.localStorage.removeItem("gameState");
      }
    }
  } catch (e) {}

  var supported = this.localStorageSupported();
  this.storage = supported ? window.localStorage : window.fakeStorage;
}

LocalStorageManager.prototype.localStorageSupported = function () {
  var testKey = "test";

  try {
    var storage = window.localStorage;
    storage.setItem(testKey, "1");
    storage.removeItem(testKey);
    return true;
  } catch (error) {
    return false;
  }
};

// Best score getters/setters
LocalStorageManager.prototype.getBestScore = function () {
  return this.storage.getItem(this.bestScoreKey) || 0;
};

LocalStorageManager.prototype.setBestScore = function (score) {
  this.storage.setItem(this.bestScoreKey, score);
};

// Game state getters/setters and clearing
LocalStorageManager.prototype.getGameState = function () {
  var stateJSON = this.storage.getItem(this.gameStateKey);
  return stateJSON ? JSON.parse(stateJSON) : null;
};

LocalStorageManager.prototype.setGameState = function (gameState) {
  this.storage.setItem(this.gameStateKey, JSON.stringify(gameState));
};

LocalStorageManager.prototype.clearGameState = function () {
  this.storage.removeItem(this.gameStateKey);
};
