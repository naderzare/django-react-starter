import React, { useState } from "react";
import axios from "../axiosConfig";

type AddSampleModalProps = {
  onClose: () => void;
  onSampleAdded: () => void; // Callback to refresh the sample list
};

const AddSampleModal: React.FC<AddSampleModalProps> = ({ onClose, onSampleAdded }) => {
  const [name, setname] = useState<string>("");
  const [age, setAge] = useState<number | "">("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post("/api/add", { name, age });
      onSampleAdded();
      onClose();
    } catch (error) {
      console.error("Error adding sample:", error);
    }
  };

  return (
    <div
      className="modal show d-block"
      tabIndex={-1}
      style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }}
    >
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Add Sample</h5>
            <button
              type="button"
              className="btn-close"
              onClick={onClose}
            ></button>
          </div>
          <div className="modal-body">
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label" htmlFor="name">
                  Name
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="name"
                  value={name}
                  onChange={(e) => setname(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label" htmlFor="age">
                  Age
                </label>
                <input
                  type="number"
                  className="form-control"
                  id="age"
                  value={age}
                  onChange={(e) => setAge(Number(e.target.value))}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary">
                Add Sample
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddSampleModal;
