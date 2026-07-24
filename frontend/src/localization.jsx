import { createContext, useContext, useState } from 'react';

const translations = {
  nl: {
    brand: 'Allergenen Check',
    pageTitle: 'Product Allergieën',
    loading: 'Producten laden...',
    noAllergens: 'Geen bekende allergenen',
    footer: 'Product Allergieën',
  },
  en: {
    brand: 'Allergen Check',
    pageTitle: 'Product Allergies',
    loading: 'Loading products...',
    noAllergens: 'No known allergens',
    footer: 'Product Allergies',
  },
};

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('nl');
  const t = translations[language];

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}