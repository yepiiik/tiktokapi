import React, { useState } from 'react';

function App() {
  const [views, setViews] = useState("Enter music ID");
  const [musicIdValue, setMusicIdValue] = useState()

  function analyze() {
    let xhr = new XMLHttpRequest();
    xhr.open('get', 'http://192.168.0.175:80/api/music_statistic/' + musicIdValue);
    xhr.send();
    setViews("Please wait")
    xhr.onload = function() {
      setViews(this.responseText)
    }
  }

  return (
    <div className='App'>
      <h1>{views}</h1>
      <input
        type='text'
        value={musicIdValue}
        onChange={event => setMusicIdValue(event.target.value)}
        />
        <button onClick={analyze}>Analyze</button>
    </div>
  );
}

export default App;
