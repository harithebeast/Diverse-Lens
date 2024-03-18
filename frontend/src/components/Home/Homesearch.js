import React, { useState } from "react";
import { BiSearch } from 'react-icons/bi';

function HomeSearch() {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearch = (event) => {
    if (event.key === "Enter") {
      // Simulate search logic (replace with your actual search functionality)
      console.log(`Search Term: ${searchTerm}`);
      setSearchTerm(""); // Clear the search term after submission
    }
  };

  return (
    <div className="search-container text-center mb-4">
      <input
        type="text"
        placeholder="Search"
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
        onKeyDown={handleSearch} // Handle Enter key press
        style={{
          padding: "10px",
          border: "2px solid #ddd",
          borderRadius: "5px",
          fontSize: "16px",
          width: "450px",
          height: "25px",
        }}
      />
      <BiSearch className="searchIcon" style={{ marginLeft: '-35px', fontSize: '20px', color: '#888', cursor: 'pointer' }} />
    </div>
  );
}

export default HomeSearch;
