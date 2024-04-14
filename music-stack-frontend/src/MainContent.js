import React from 'react';

function MainContent({ searchResults, apiType }) {
  const renderContent = () => {
    switch (apiType) {
      case 'albums':
        return searchResults.map((item, index) => (
          <li key={index}>{item.AlbumTitle} - Rating: {item.AvgRating}</li>
        ));
      case 'recommendations':
        return searchResults.map((item, index) => (
          <li key={index}>{item.AlbumTitle} by {item.ArtistName}</li>
        ));
      case 'tracks':
        return searchResults.map((item, index) => (
          <li key={index}>{item.TrackName} - Rating: {item.AvgRating}</li>
        ));
      case 'follow':
        return searchResults.map((item, index) => (
          <li key={index}>{item.AlbumTitle} - Avg Rating: {item.AvgRating}</li>
        ));
      default:
        return <li>No data available</li>;
    }
  };

  return (
    <div className="main-content">
      <h2>Results</h2>
      <ul>{renderContent()}</ul>
    </div>
  );
}

export default MainContent;
