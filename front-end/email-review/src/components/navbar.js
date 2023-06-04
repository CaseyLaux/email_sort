import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/inbox">Inbox</Link>
        </li>
        <li>
          <Link to="/sortedinbox">Sorted Inbox</Link>
        </li>
        <li>
          <Link to="/unsortedinbox">Unsorted Inbox</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
