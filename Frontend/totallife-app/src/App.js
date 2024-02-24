import React, { useState, useEffect } from 'react';

const AppointmentList = () => {
  // State variables to manage appointments and filters
  const [appointments, setAppointments] = useState([]);
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  // Fetch appointments from the API when the component mounts
  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/appointments/');
        const data = await response.json();
        setAppointments(data);
        setFilteredAppointments(data);
      } catch (error) {
        console.error('Error fetching appointments:', error);
      }
    };

    fetchAppointments();
  }, []);

  // Handle filtering appointments based on selected date range
  const handleFilter = () => {
    if (startDate && endDate) {
      const filtered = appointments.filter(appointment => {
        const appointmentDate = new Date(appointment.appointment_date);
        return appointmentDate >= new Date(startDate) && appointmentDate <= new Date(endDate);
      });
      setFilteredAppointments(filtered);
    } else {
      setFilteredAppointments(appointments);
    }
  };

  // Reset filters and show all appointments
  const handleResetFilters = () => {
    setStartDate('');
    setEndDate('');
    setFilteredAppointments(appointments);
  };

  return (
    <div className="container mx-auto mt-8 dark bg-gray-900 text-white rounded">
      {/* Header */}
      <h1 className="text-2xl font-bold mb-4 text-center">Appointment List</h1>

      {/* Filter Section */}
      <div className="flex justify-between mb-6 px-4">
        <div className="flex items-center ml-4">
          <label className="mr-2">Start Date:</label>
          <input
            type="date"
            value={startDate}
            onChange={e => setStartDate(e.target.value)}
            className="border rounded p-1 bg-white text-gray-800"
          />
        </div>
        <div className="flex items-center ml-4">
          <label className="mr-2">End Date:</label>
          <input
            type="date"
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
            className="border rounded p-1 bg-white text-gray-800"
          />
        </div>
        <div className="flex items-center ml-4">
          <button onClick={handleFilter} className="bg-blue-500 text-white px-4 py-2 rounded ml-4 hover:bg-blue-700">
            Filter Appointments
          </button>
          <button onClick={handleResetFilters} className="bg-gray-500 text-white px-4 py-2 rounded ml-4 hover:bg-gray-700">
            Reset Filters
          </button>
        </div>
      </div>

      {/* List of Appointments */}
      <ul>
        {filteredAppointments.map(appointment => (
          <li key={appointment.id} className="mb-6">
            <div className="border p-4 rounded-lg bg-gray-800 text-white">
              {/* Patient Information */}
              <h2 className="text-xl font-bold mb-2">Patient Name: {appointment.patient_name}</h2>
              {/* Appointment Details */}
              <p className="mb-2">Appointment Date: {new Date(appointment.appointment_date).toLocaleString()}</p>
              <p className="mb-2">Duration: {appointment.duration_minutes} minutes</p>
              <p className="mt-2">Description: {appointment.reason_for_visit}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AppointmentList;







