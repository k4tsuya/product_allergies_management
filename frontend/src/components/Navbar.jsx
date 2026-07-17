import { t } from '../localization';

function Navbar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">{t.brand}</span>
    </nav>
  );
}

export default Navbar;