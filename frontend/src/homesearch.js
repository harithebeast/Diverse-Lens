import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import axios from 'axios';

function Login() {
  const [news, setNews] = useState('');
  const [response, setResponse] = useState(null); // Added state for response

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('/call_llm', { // Corrected axios.post
        corpus: news // Fixed variable name and object structure
      });
      setResponse(response.data); // Update state with the response data
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      // Handle cleanup or reset form if needed
      setNews(''); // Reset input field after submission
    }
  }

  return (
    <div className="login-container">
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Form onSubmit={handleSubmit}>
          <h1 className="text-center mb-4" style={{ color: '#ffffee' }}>ENTER THE NEWS</h1>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label style={{ color: '#ffffee' }}>News</Form.Label> {/* Added label text */}
            <Form.Control
              type="text"
              placeholder="Enter news"
              value={news}
              onChange={(e) => setNews(e.target.value)}
            />
          </Form.Group>
          <Button variant="primary" type="submit">Submit</Button>
        </Form>
      </div>
    </div>
  );
}

export default Login;
