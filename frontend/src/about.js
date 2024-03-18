import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBookOpen, faMagnifyingGlass, faUsers, faLightbulb } from '@fortawesome/free-solid-svg-icons';

function About() {
  return (
    <div className="about-page vh=150" style={{ color: 'white', margin: '108px 0px' }}>
      <Container>
        <Row className="justify-content-center">
          <Col md={8} className="text-center mb-5">
            <h1 className="display-4 mb-4">About DiverseLens</h1>
            <p style={{color:'#ffffff'}}>
              Welcome to DiverseLens, your go-to platform for combating bias, fostering
              critical thinking, and promoting media literacy in the digital age. At
              DiverseLens, we believe that a well-informed society is built on access to diverse
              viewpoints, critical analysis, and a commitment to truth. In an era where
              misinformation and echo chambers threaten to undermine the integrity of public
              discourse, our mission is to empower individuals to navigate the complex
              landscape of news and information with confidence and clarity.
            </p>
          </Col>
        </Row>

        <Row>
          <Col md={4}>
            <h3 className="mb-3">Our Mission</h3>
            <p>
              Our mission at DiverseLens is simple: to provide users with the tools,
              resources, and community support they need to become discerning consumers of
              news and information. We believe that by promoting exposure to diverse
              perspectives, encouraging critical thinking, and fostering a culture of media
              literacy, we can build a more resilient and informed society.
            </p>
          </Col>
          <Col md={4}>
            <h3 className="mb-3">What We Do</h3>
            <ul className="list-unstyled">
              <li>
                <FontAwesomeIcon icon={faMagnifyingGlass} className="me-2" />
                Bias Detection
              </li>
              <li>
                <FontAwesomeIcon icon={faBookOpen} className="me-2" />
                Fake News Detection
              </li>
              <li>
                <FontAwesomeIcon icon={faLightbulb} className="me-2" />
                Personalized Recommendations
              </li>
              <li>
                <FontAwesomeIcon icon={faUsers} className="me-2" />
                Critical Thinking Prompts
              </li>
              <li>
                <FontAwesomeIcon icon={faUsers} className="me-2" />
                Community Engagement
              </li>
            </ul>
          </Col>
          <Col md={4}>
            <h3 className="mb-3">Join Us</h3>
            <p>
              Join us in our mission to combat bias, promote critical thinking, and build a
              more informed society. Whether you're a seasoned news consumer or just
              beginning to explore the complexities of the media landscape, DiverseLens is
              here to support you every step of the way. Together, we can navigate the
              challenges of the digital age and build a future where truth, diversity, and
              critical thinking prevail. Welcome to DiverseLens.
            </p>
          </Col>
        </Row>

        <Row className="mt-5 justify-content-center">
          <Col md={6} className="text-center">
            <p>Contact us on:</p>
            <p>
              Email: DiverseLens@gmail.com <br />
              Ph.no: 9854763212
            </p>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default About;
