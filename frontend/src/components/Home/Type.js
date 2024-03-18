import React from "react";
import Typewriter from "typewriter-effect";

function Type() {
  return (
    <Typewriter 
      options={{
        strings: [
          "Bias-Free, Diverse, Informed.",
          "Discover, Balance, Empower,Engage.",
          "Personalized, Balanced, Informed, Aware.",
        ],
        autoStart: true,
        loop: true,
        deleteSpeed: 20,
      }}
    />
  );
}

export default Type;
