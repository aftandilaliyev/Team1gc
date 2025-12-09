'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Navigation from '../../../components/Navigation.jsx';
import { client } from '../../../lib/api.jsx';

export default function SupplierDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [pendingOrders, setPendingOrders] = useState([]);
  const [allOrders, setAllOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [actionLoading, setActionLoading] = useState(false);
  const router = useRouter();

  const fetchAnalytics = async () => {
    try {
      const response = await client.supplierApi.getSupplierAnalyticsApiV1SuppliersAnalyticsGet();
      setAnalytics(response.data);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
      if (err.response?.status === 401) {
        router.push('/login');
      }
    }
  };

  const fetchPendingOrders = async () => {
    try {
      const response = await client.supplierApi.getOrdersForApprovalApiV1SuppliersOrdersPendingGet();
      setPendingOrders(response.data);
    } catch (err) {
      console.error('Failed to fetch pending orders:', err);
      if (err.response?.status === 401) {
        router.push('/login');
      }
    }
  };

  const fetchAllOrders = async () => {
    try {
      const response = await client.supplierApi.getAllOrdersApiV1SuppliersOrdersGet();
      setAllOrders(response.data);
    } catch (err) {
      console.error('Failed to fetch all orders:', err);
      if (err.response?.status === 401) {
        router.push('/login');
      }
    }
  };

  const fetchOrderDetails = async (orderId) => {
    try {
      const response = await client.supplierApi.getOrderApiV1SuppliersOrdersOrderIdGet(orderId);
      setSelectedOrder(response.data);
    } catch (err) {
      alert('Failed to load order details');
      console.error(err);
    }
  };

  const approveOrder = async (orderId) => {
    setActionLoading(true);
    try {
      await client.supplierApi.approveOrderApiV1SuppliersOrdersOrderIdApprovePost(orderId);
      alert('Order approved successfully!');
      await fetchPendingOrders();
      await fetchAllOrders();
      await fetchAnalytics();
    } catch (err) {
      alert('Failed to approve order');
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  const updateOrderStatus = async (orderId, status, addresses = {}) => {
    setActionLoading(true);
    try {
      const updateData = {
        status,
        ...addresses
      };
      await client.supplierApi.updateOrderStatusApiV1SuppliersOrdersOrderIdPut(orderId, updateData);
      alert(`Order ${status} successfully!`);
      await fetchAllOrders();
      await fetchAnalytics();
      if (selectedOrder?.id === orderId) {
        await fetchOrderDetails(orderId);
      }
    } catch (err) {
      alert(`Failed to ${status} order`);
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([
        fetchAnalytics(),
        fetchPendingOrders(),
        fetchAllOrders()
      ]);
      setLoading(false);
    };
    
    loadData();
  }, []);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'confirmed':
        return 'bg-blue-100 text-blue-800';
      case 'shipped':
        return 'bg-purple-100 text-purple-800';
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusActions = (order) => {
    const actions = [];
    
    if (order.status === 'confirmed') {
      actions.push(
        <button
          key="approve"
          onClick={() => approveOrder(order.id)}
          disabled={actionLoading}
          className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          Approve & Ship
        </button>
      );
    }
    
    if (order.status === 'shipped') {
      actions.push(
        <button
          key="deliver"
          onClick={() => updateOrderStatus(order.id, 'delivered')}
          disabled={actionLoading}
          className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 disabled:opacity-50"
        >
          Mark Delivered
        </button>
      );
    }
    
    if (['pending', 'confirmed', 'shipped'].includes(order.status)) {
      actions.push(
        <button
          key="cancel"
          onClick={() => updateOrderStatus(order.id, 'cancelled')}
          disabled={actionLoading}
          className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 disabled:opacity-50"
        >
          Cancel
        </button>
      );
    }
    
    return actions;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <div className="flex justify-center items-center h-64">
          <div className="text-lg">Loading supplier dashboard...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Supplier Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage orders and track business performance</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Tab Navigation */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'overview', name: 'Overview' },
              { id: 'pending', name: 'Pending Approval' },
              { id: 'all-orders', name: 'All Orders' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.name}
                {tab.id === 'pending' && analytics?.orders_needing_approval > 0 && (
                  <span className="ml-2 bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    {analytics.orders_needing_approval}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && analytics && (
          <div className="space-y-6">
            {/* Analytics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Orders</p>
                    <p className="text-2xl font-semibold text-gray-900">{analytics.total_orders}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-yellow-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Awaiting Approval</p>
                    <p className="text-2xl font-semibold text-gray-900">{analytics.orders_needing_approval}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Delivered</p>
                    <p className="text-2xl font-semibold text-gray-900">{analytics.delivered_orders}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-indigo-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                    <p className="text-2xl font-semibold text-gray-900">{formatPrice(analytics.total_revenue)}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Status Breakdown */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Order Status Breakdown</h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">{analytics.pending_orders}</div>
                  <div className="text-sm text-gray-600">Pending</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{analytics.confirmed_orders}</div>
                  <div className="text-sm text-gray-600">Confirmed</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{analytics.shipped_orders}</div>
                  <div className="text-sm text-gray-600">Shipped</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{analytics.delivered_orders}</div>
                  <div className="text-sm text-gray-600">Delivered</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{analytics.cancelled_orders}</div>
                  <div className="text-sm text-gray-600">Cancelled</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Pending Orders Tab */}
        {activeTab === 'pending' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">Orders Awaiting Approval</h2>
              <button
                onClick={fetchPendingOrders}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
              >
                Refresh
              </button>
            </div>

            {pendingOrders.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg">No orders awaiting approval</div>
              </div>
            ) : (
              <div className="space-y-4">
                {pendingOrders.map((order) => (
                  <div key={order.id} className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          Order #{order.id.slice(0, 8)}
                        </h3>
                        <p className="text-sm text-gray-600">
                          Placed on {formatDate(order.created_at)}
                        </p>
                      </div>
                      <div className="text-right">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(order.status)}`}>
                          {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                        </span>
                        <p className="text-lg font-semibold text-gray-900 mt-1">
                          {formatPrice(order.total_amount)}
                        </p>
                      </div>
                    </div>

                    <div className="flex justify-between items-center">
                      <button
                        onClick={() => fetchOrderDetails(order.id)}
                        className="text-indigo-600 hover:text-indigo-800 font-medium"
                      >
                        View Details
                      </button>
                      <div className="space-x-2">
                        {getStatusActions(order)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* All Orders Tab */}
        {activeTab === 'all-orders' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-900">All Orders</h2>
              <button
                onClick={fetchAllOrders}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
              >
                Refresh
              </button>
            </div>

            {allOrders.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg">No orders found</div>
              </div>
            ) : (
              <div className="space-y-4">
                {allOrders.map((order) => (
                  <div key={order.id} className="bg-white rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          Order #{order.id.slice(0, 8)}
                        </h3>
                        <p className="text-sm text-gray-600">
                          Placed on {formatDate(order.created_at)}
                        </p>
                        <p className="text-sm text-gray-600">
                          Customer ID: {order.user_id}
                        </p>
                      </div>
                      <div className="text-right">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(order.status)}`}>
                          {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                        </span>
                        <p className="text-lg font-semibold text-gray-900 mt-1">
                          {formatPrice(order.total_amount)}
                        </p>
                      </div>
                    </div>

                    <div className="flex justify-between items-center">
                      <button
                        onClick={() => fetchOrderDetails(order.id)}
                        className="text-indigo-600 hover:text-indigo-800 font-medium"
                      >
                        View Details
                      </button>
                      <div className="space-x-2">
                        {getStatusActions(order)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Order Details Modal */}
        {selectedOrder && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Order Details #{selectedOrder.id.slice(0, 8)}
                  </h3>
                  <button
                    onClick={() => setSelectedOrder(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  <div>
                    <p><strong>Status:</strong> <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(selectedOrder.status)}`}>
                      {selectedOrder.status.charAt(0).toUpperCase() + selectedOrder.status.slice(1)}
                    </span></p>
                    <p><strong>Customer ID:</strong> {selectedOrder.user_id}</p>
                    <p><strong>Total:</strong> {formatPrice(selectedOrder.total_amount)}</p>
                    <p><strong>Order Date:</strong> {formatDate(selectedOrder.created_at)}</p>
                    <p><strong>Shipping Address:</strong> {selectedOrder.shipping_address || 'Not provided'}</p>
                    <p><strong>Billing Address:</strong> {selectedOrder.billing_address || 'Not provided'}</p>
                  </div>
                  
                  {selectedOrder.items && selectedOrder.items.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2">Items:</h4>
                      {selectedOrder.items.map((item) => (
                        <div key={item.id} className="border-b pb-2 mb-2 last:border-b-0">
                          <p><strong>Product:</strong> {item?.product?.name || `Product ${item.product_id}`}</p>
                          <p>Quantity: {item.quantity} × {formatPrice(item.price_at_time)}</p>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  <div className="flex justify-end space-x-2 pt-4 border-t">
                    {getStatusActions(selectedOrder)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
