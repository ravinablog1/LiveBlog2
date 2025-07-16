import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Index from './views/core/Index';
import About from './views/pages/About';
import Contact from './views/pages/Contact';
import Login from './views/auth/Login';
import Register from './views/auth/Register';
import AddPost from './views/dashboard/AddPost';
import EditPost from './views/dashboard/EditPost';
import Dashboard from './views/dashboard/Dashboard';
import Posts from './views/dashboard/Posts';
import Comments from './views/dashboard/Comments';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/about/" element={<About />} />
        <Route path="/contact/" element={<Contact />} />
        <Route path="/login/" element={<Login />} />
        <Route path="/register/" element={<Register />} />
        <Route path="/dashboard/" element={<Dashboard />} />
        <Route path="/posts/" element={<Posts />} />
        <Route path="/add-post/" element={<AddPost />} />
        <Route path="/edit-post/:id/" element={<EditPost />} />
        <Route path="/comments/" element={<Comments />} />
      </Routes>
    </Router>
  );
}

export default App;
