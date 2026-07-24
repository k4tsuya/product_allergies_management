import { useLanguage } from '../localization.jsx';

function Navbar() {
  const { language, setLanguage, t } = useLanguage();

  return (
    <nav className="navbar">
      <span className="navbar-brand">{t.brand}</span>
      <div className="navbar-links">
        
        <a  href={`http://localhost:8000/products/pdf?language=${language}`}
          className="navbar-link"
        >
          Download PDF
        </a>
        <button
          onClick={() => setLanguage(language === 'nl' ? 'en' : 'nl')}
          className="language-switcher"
        >
          {language === 'nl' ? 'NL' : 'EN'}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;