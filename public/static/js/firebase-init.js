import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyDJF27z4gx7TArB2JkCrUL1uzaHB2vOyTs",
  authDomain: "hospital-management-14cbe.firebaseapp.com",
  projectId: "hospital-management-14cbe",
  storageBucket: "hospital-management-14cbe.firebasestorage.app",
  messagingSenderId: "1063176547414",
  appId: "1:1063176547414:web:68a9e0988c1d412aff9ff7",
  measurementId: "G-8R84143G4Q"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
