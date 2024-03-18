import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom'; // Import Link for navigation

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
      event.preventDefault();
      // Simulate login logic (replace with your actual authentication)
      console.log(`Username: ${username}, Password: ${password}`);
      setUsername('');
      setPassword('');
    };

  return (
    <div className="login-container">
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Form onSubmit={handleSubmit}>
          <h1 className="text-center mb-4" style={{ color: '#ffffee' }}>LOGIN</h1>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label style={{ color: '#ffffee' }}>Email ID</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label style={{ color: '#ffffee' }}>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3 d-flex justify-content-between">
            <Form.Check type="checkbox" label="Remember me" style={{ color: '#ffffee' }} />
            <a href="#">Forgot Password?</a>
          </Form.Group>
          <Button variant="primary" type="submit">
            LOGIN
          </Button>

          <p className="mt-3 text-center" style={{ color: '#ffffee' }} >
            Don't have an account?{' '}
            <Link to="/signup">Sign Up</Link>
          </p>
        </Form>
      </div>
    </div>
  );
}

export default Login;
