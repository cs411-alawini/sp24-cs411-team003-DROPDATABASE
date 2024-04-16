import React, { useState } from 'react';
import axios from 'axios';
import Header from './Header';
import SearchBar from './SearchBar';
import MainContent from './MainContent';
import './App.css';

function App() {
  const [searchResults, setSearchResults] = useState([]);
  const [currentApi, setCurrentApi] = useState('albums');

  const fetchData = (apiPath, params) => {
    axios.get(`http://localhost:5000/${apiPath}`, { params })
      .then(response => {
        console.log(response.data);
        setSearchResults(response.data);
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  };

  const handleSearch = (searchTerm) => {
    let apiPath;
    switch (currentApi) {
      case 'albums':
        apiPath = `top5_albums_by_genre/${searchTerm}`;
        break;
      case 'recommendations':
        apiPath = `user_recommendations_by_artist/${searchTerm}`;
        break;
      case 'tracks':
        apiPath = 'most_popular_tracks';
        break;
      case 'follow':
        apiPath = `recommend_album_by_follow/${searchTerm}`;
        break;
      default:
        return;
    }
    fetchData(apiPath, { userId: searchTerm });
  };

  return (
    <div className="App">
      <Header />
      <div>
        <button onClick={() => setCurrentApi('albums')}>Top Albums by Genre</button>
        <button onClick={() => setCurrentApi('recommendations')}>Recommendations by Artist</button>
        <button onClick={() => setCurrentApi('tracks')}>Most Popular Tracks</button>
        <button onClick={() => setCurrentApi('follow')}>Recommendations by Follow</button>
      </div>
      <SearchBar onSearch={handleSearch} />
      <MainContent searchResults={searchResults} apiType={currentApi} />
    </div>
  );
}

export default App;
