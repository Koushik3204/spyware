import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div>
      <Navbar className="bg" data-bs-theme="dark">
        <Container>
          <Navbar.Brand className="text-dark fw-bold">Spyware Web App</Navbar.Brand>
            <Nav.Link className="fw-bold" as={Link} to="/Login">
              Login
            </Nav.Link>
        </Container>
      </Navbar>
      <div className="home"></div>
    </div>
  );
}
