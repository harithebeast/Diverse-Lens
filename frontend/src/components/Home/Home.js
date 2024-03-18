import React, { useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { BiSearch } from 'react-icons/bi';

import Particle from "../Particle";
import Type from "./Type";



function Home() {
  const [query, setQuery] = useState(""); // State for search query

  return (
    <section>
      <Container fluid className="home-section" id="home">
        <Particle />
        <Container className="home-content">
        
          <Row>
            <Col md={7} className="home-header">
              <h1 style={{ paddingBottom: '15px', fontSize: '.5rem'}} className="heading">
                Hi There!{" "}
                <span className="wave" role="img" aria-labelledby="wave">
                  👋🏻
                </span>
              </h1>

              <h1 className="heading-name ">
                This Is
                <strong className="main-name" style={{ color: '#8C52FF' }}> DiverseLens !!</strong>
              </h1>

              <div style={{ padding: '50px', textAlign: 'left',}}>
               <strong >
               <Type />
                </strong> 
              </div>
            </Col>

            <Col md={5} style={{ paddingBottom: '20px' }}>
              <img
                src="https://www.netclues.com/caches/926x746/2023-08-29-06-19-31-reactjs-development-company.png"
                alt="home pic"
                className="img-fluid"
                style={{ maxHeight: '450px' }}
              />
            </Col>
          </Row>
        </Container>
      </Container>
    </section>
  );
}

export default Home;
