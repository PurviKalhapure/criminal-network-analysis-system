import React, { useState } from 'react';
import GraphView from './GraphView';
import './App.css';

function App() {
  const [searchId, setSearchId] = useState('P0');
  const [inputValue, setInputValue] = useState('P0');

  const handleSearch = () => {
    setSearchId(inputValue);
  };

  return (
    <div className="dashboard">
      <header className="topbar">
        <h1>⚡ CRIME NETWORK INTELLIGENCE</h1>
        <div className="search-box">
          <input
            placeholder="Enter Person ID (e.g. P0, P1...)"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch}>Search</button>
        </div>
      </header>
      <div className="main-layout">
        <main className="graph-container">
          <GraphView personId={searchId} />
        </main>
      </div>
    </div>
  );
}

export default App;