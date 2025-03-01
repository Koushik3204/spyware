import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { Button, Container,  Navbar } from "react-bootstrap";
import { baseurl } from "./App";


export default function Login() {
  const [userid, setUserid] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault(); 
    if (!userid || !password) {
      alert('Please fill all fields');
      return;
    }

    try {
      const response = await axios.post(
        baseurl,
        new URLSearchParams({
          tag: "adminlogin",
          email: userid,
          password: password,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      if (response.data && response.data.error === 0) {
        console.log(response.data);
        sessionStorage.setItem('user', JSON.stringify(response.data));
        alert("Login successfully");
        navigate('/dashboard');
      } else {
        alert(response.data.message || "Invalid credentials");
      }
    } catch (error) {
      alert(error.response?.data?.message || "An error occurred. Please try again.");
    }
  };

  return (
    <div>
      <div className="login-container">
        <div className="card1 shadow ">
          <h2 className=" text-center">Login</h2>
          <form>
            <label>Admin Email</label>
            <input
              type="text"
              name="username"
              value={userid}
              className="form-control mb-3"
              onChange={(e) => setUserid(e.target.value)}
              required
            />
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={password}
              className="form-control mb-3"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <div className="d-flex gap-4 mx-auto ">
              <Button variant="warning" onClick={handleLogin}>
                Login
              </Button>
              <Button variant="dark" to="/" as={Link}>
                Back
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
