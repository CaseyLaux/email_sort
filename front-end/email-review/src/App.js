import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar';
import Inbox from './Inbox';
import SortedInbox from './SortedInbox';
import UnsortedInbox from './UnsortedInbox';
 
import EmailViewer from './EmailViewer';
import "./index.css"


function App() {
  
  return (
    <div className="App">
      
      <EmailViewer/>
    </div>
  );
}

export default App;