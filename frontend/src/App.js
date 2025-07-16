import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Index from './views/core/Index';
import About from './views/pages/About';
import Contact from './views/pages/Contact';
// ... other imports

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/about/" element={<About />} />
        <Route path="/contact/" element={<Contact />} />
        {/* ... other routes */}
      </Routes>
    </Router>
  );
}

export default App;