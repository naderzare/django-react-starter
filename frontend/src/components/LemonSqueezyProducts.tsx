import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { paymentService } from '../services/paymentService';

type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
};

const LemonSqueezyProducts: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const result = await paymentService.getProducts();
      setProducts(result);
    } catch (error: any) {
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleBuy = async (productId: string) => {
    try {
      // Call createPayment in your service
      const response = await paymentService.createPayment(productId);
      // response should include a "checkout_url"
      window.location.href = response.checkout_url;
    } catch (error: any) {
      toast.error('Error creating payment');
    }
  };

  if (loading) {
    return (
      <div className="text-center my-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!loading && products.length === 0) {
    return <div className="alert alert-info">No products found</div>;
  }

  return (
    <div className="container my-4">
      <h2>Products</h2>
      <div className="row">
        {products.map((product) => (
          <div className="col-md-4" key={product.id}>
            <div className="card mb-3">
              <div className="card-body">
                <h4 className="card-title">{product.name}</h4>
                <p className="card-text">{product.description}</p>
                <p><strong>Price:</strong> ${product.price}</p>
                <button 
                  onClick={() => handleBuy(product.id)} 
                  className="btn btn-primary"
                >
                  Buy
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LemonSqueezyProducts;
