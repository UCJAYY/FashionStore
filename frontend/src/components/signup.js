// src/components/Signup.js

import React, { useState } from 'react';
import axios from 'axios';

const Signup = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    age_range: '',
    gender: '',
    profession: '',
    hobbies: '',
    location: '',
    clothing_size: '',
    preferred_style: '',
    budget: '',
    favorite_colors: '',
    occasions: '',
    brand_preferences: '',
    body_type: '',
    favorite_influencers: '',
    sustainability_preference: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Replace with your backend signup URL
      const response = await axios.post('http://localhost:8000/api/signup/', formData);
      console.log('Signup successful:', response.data);
    } catch (error) {
      console.error('Signup error:', error);
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {/* Add additional input fields for the rest of your form */}
        <input
          type="text"
          name="age_range"
          placeholder="Age Range (e.g., 25-34)"
          value={formData.age_range}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="gender"
          placeholder="Gender"
          value={formData.gender}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="profession"
          placeholder="Profession"
          value={formData.profession}
          onChange={handleChange}
          required
        />
        <textarea
          name="hobbies"
          placeholder="Hobbies"
          value={formData.hobbies}
          onChange={handleChange}
          required
        />
        {/* Continue adding fields for location, clothing_size, etc. */}
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Signup;
