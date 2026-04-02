import React from 'react';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import HomePage from './pages/HomePage/HomePage';
import './assets/styles/global.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main className="main-content">
        <HomePage />
      </main>
      <Footer />
    </div>
  );
}

export default App;