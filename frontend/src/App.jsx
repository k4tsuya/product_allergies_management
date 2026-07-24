import { Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AllergensPage from './pages/AllergensPage';

function App() {
  return (
    <div className="page">
      <Navbar />

      <Routes>
        <Route path="/" element={<AllergensPage />} />
      </Routes>

      <Footer />
    </div>
  );
}

export default App;