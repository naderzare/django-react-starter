import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { PaymentTransaction } from '../types/auth';
import { paymentService } from '../services/paymentService';
import LemonSqueezyProducts from '../components/LemonSqueezyProducts';

const PaymentsPage: React.FC = () => {
  const [transactions, setTransactions] = useState<PaymentTransaction[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const transactions = await paymentService.getPaymentHistory();
      setTransactions(transactions);
    } catch (error: any) {
      if (error.response?.status === 401) {
        toast.error('Please login to view your payment history');
        navigate('/');
      } else {
        toast.error('Failed to load payment history');
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-success';
      case 'processing':
        return 'bg-warning';
      case 'pending':
        return 'bg-info';
      case 'failed':
        return 'bg-danger';
      default:
        return 'bg-secondary';
    }
  };

  return (
    <div>
      <LemonSqueezyProducts />
      
      <div className="container mt-5">
        <h2 className="mb-4">Payment History</h2>
        
        {loading ? (
          <div className="text-center my-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : transactions.length === 0 ? (
          <div className="alert alert-info">
            You have no payment transactions yet. Buy some credits to get started!
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td>{transaction.transaction_id}</td>
                    <td>
                      {transaction.currency} $
                      {typeof transaction.amount === 'number' 
                        ? transaction.amount.toFixed(2) 
                        : parseFloat(String(transaction.amount)).toFixed(2)}
                    </td>
                    <td>
                      <span className={`badge ${getStatusBadgeClass(transaction.status)}`}>
                        {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                      </span>
                    </td>
                    <td>{new Date(transaction.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentsPage;