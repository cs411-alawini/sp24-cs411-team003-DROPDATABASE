import React from 'react';

function Header() {
  return (
    <header className="header">
      <img src="./logo.png" alt="Music Stack Logo" className="logo" />
      <nav className="navigation">
        <a href="#about">About Us</a>
        <a href="#login">Login</a>
      </nav>
    </header>
  );
}

export default Header;
