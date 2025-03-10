import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../axiosConfig";
import AddSampleModal from "../components/AddSampleModal";
import toast from "react-hot-toast";

type Sample = {
  id: number;
  name: string;
  age: number;
};

const SampleList: React.FC = () => {
  const [samples, setSamples] = useState<Sample[]>([]);
  const [showAddSampleModal, setShowAddSampleModal] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const user = localStorage.getItem('user');
    if (!user) {
      toast.error('Please login to view samples');
      navigate('/');
      return;
    }
    fetchSamples();
  }, [navigate]);

  const fetchSamples = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Sample[]>("/api/api/all");
      setSamples(response.data);
    } catch (error: any) {
      if (error.response?.status === 401) {
        toast.error('Session expired. Please login again');
        navigate('/');
      } else {
        toast.error('Error fetching samples');
      }
      console.error("Error fetching samples:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Sample List</h2>
        <button
          className="btn btn-primary"
          onClick={() => setShowAddSampleModal(true)}
        >
          Add Sample
        </button>
      </div>

      {loading ? (
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      ) : samples.length === 0 ? (
        <div className="alert alert-info">No samples found</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-bordered table-hover">
            <thead className="table-light">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
              </tr>
            </thead>
            <tbody>
              {samples.map((sample) => (
                <tr key={sample.id}>
                  <td>{sample.id}</td>
                  <td>{sample.name}</td>
                  <td>{sample.age}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showAddSampleModal && (
        <AddSampleModal
          onClose={() => setShowAddSampleModal(false)}
          onSampleAdded={() => {
            fetchSamples();
            toast.success('Sample added successfully');
          }}
        />
      )}
    </div>
  );
};

export default SampleList;
