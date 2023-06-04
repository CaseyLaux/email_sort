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
      <Router>
      <Navbar />
      <Routes>
        <Route path="/inbox" element={<Inbox />} />
        <Route path="/sortedinbox" element={<SortedInbox />} />
        <Route path="/unsortedinbox" element={<UnsortedInbox />} />
      </Routes>
    </Router>
      <EmailViewer/>
    </div>
  );
}

export default App;