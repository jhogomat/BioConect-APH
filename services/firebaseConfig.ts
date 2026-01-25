// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBXgUNRluvBtwTbkuKfuslYyYcBESvVMlo",
  authDomain: "bioconect-aph.firebaseapp.com",
  projectId: "bioconect-aph",
  storageBucket: "bioconect-aph.firebasestorage.app",
  messagingSenderId: "505766037828",
  appId: "1:505766037828:web:321317fb237597f5016f11",
  measurementId: "G-4W5FR612EJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
