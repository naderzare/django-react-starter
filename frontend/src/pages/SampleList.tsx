import React, { useState, useEffect } from "react";
import axios from "../axiosConfig";
import AddSampleModal from "../components/AddSampleModal"; // Import AddSampleModal component

type Sample = {
  id: number;
  name: string;
  age: number;
};

const SampleList: React.FC = () => {
  const [samples, setSamples] = useState<Sample[]>([]);
  const [showAddSampleModal, setShowAddSampleModal] = useState<boolean>(false);

  const fetchSamples = async () => {
    try {
      const response = await axios.get<Sample[]>("/api/all");
      setSamples(response.data);
    } catch (error) {
      console.error("Error fetching samples:", error);
    }
  };

  useEffect(() => {
    fetchSamples();
  }, []);

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Sample List</h2>
      <button
        className="btn btn-primary mb-3"
        onClick={() => setShowAddSampleModal(true)}
      >
        Add Sample
      </button>
      <table className="table table-bordered table-hover">
        <thead>
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

      {/* Add Sample Modal */}
      {showAddSampleModal && (
        <AddSampleModal
          onClose={() => setShowAddSampleModal(false)}
          onSampleAdded={fetchSamples}
        />
      )}
    </div>
  );
};

export default SampleList;
