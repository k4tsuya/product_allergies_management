import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProductList from './components/ProductList';

function App() {
  return (
    <div className="page">
      <Navbar />

      <div className="app">
        <ProductList />
      </div>

      <Footer />
    </div>
  );
}

export default App;