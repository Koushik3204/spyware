
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Home from './Home';
import Login from './Login';
import AdminDashboard from './AdminDashboard';

export const baseurl = "https://yhmysore.in/api/spywareAPI.php";

function App() {
  return (
    <>
    <div>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Home />}></Route>
          <Route path='/Login' element={<Login />}></Route>
          <Route path='/dashboard' element={<AdminDashboard />}></Route>
        </Routes>
      </BrowserRouter>
    </div>
    </>
  );
}

export default App;
