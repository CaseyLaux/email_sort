// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDLdQw_JQwOVGSv5Lf53uF2Oqc3PduSWjc",
  authDomain: "siemlessemail.firebaseapp.com",
  projectId: "siemlessemail",
  storageBucket: "siemlessemail.appspot.com",
  messagingSenderId: "548875487149",
  appId: "1:548875487149:web:503037a0d5ab744855c324",
  measurementId: "G-WFHQJCPXD8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);