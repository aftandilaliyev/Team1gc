'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Navigation from '../../components/Navigation.jsx';
import { client } from '../../lib/api.jsx';

// Personal astrology quiz questions
const quizQuestions = [
  {
    id: 1,
    question: "What energy are you seeking right now?",
    options: ["Protection and grounding", "Love and compassion", "Intuition and clarity", "Success and abundance"]
  },
  {
    id: 2,
    question: "Which element resonates with you most?",
    options: ["Fire - Passion and action", "Water - Emotion and flow", "Earth - Stability and growth", "Air - Communication and freedom"]
  },
  {
    id: 3,
    question: "What time of day do you feel most connected to your spiritual self?",
    options: ["Dawn - New beginnings", "Noon - Peak energy", "Sunset - Reflection", "Midnight - Deep intuition"]
  },
  {
    id: 4,
    question: "How do you prefer to wear or carry crystals?",
    options: ["As jewelry (necklace, ring)", "In a pocket or pouch", "As a decorative piece", "As a keychain or accessory"]
  },
  {
    id: 5,
    question: "What color palette draws you in?",
    options: ["Deep blues and purples", "Greens and earth tones", "Pinks and whites", "Blacks and grays"]
  },
  {
    id: 6,
    question: "What is your primary intention with crystals?",
    options: ["Emotional healing", "Physical protection", "Spiritual growth", "Manifestation"]
  },
  {
    id: 7,
    question: "Which moon phase do you feel most aligned with?",
    options: ["New Moon - Setting intentions", "Full Moon - Releasing and celebrating", "Waxing Moon - Building energy", "Waning Moon - Letting go"]
  },
  {
    id: 8,
    question: "What size crystal piece do you prefer?",
    options: ["Small and subtle", "Medium and noticeable", "Large and statement", "Any size works"]
  }
];

// Products to search for after quiz
const productsToSearch = [
  "Keychain",
  "Brooch",
  "Rose Quartz",
  "Jasper",
  "Obsidian",
  "Moonstone",
  "Turquoise",
  "Labradorite",
  "Malachite",
  "Jade",
  "Lapis Lazuli",
  "Tiger's Eye"
];

export default function BuyerPage() {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchingProducts, setSearchingProducts] = useState(false);
  const router = useRouter();

  const handleAnswerSelect = (questionId, answerIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      setQuizCompleted(true);
      searchForProducts();
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const searchForProducts = async () => {
    setSearchingProducts(true);
    setLoading(true);
    const foundProducts = [];

    // Search for each product randomly
    const shuffledProducts = [...productsToSearch].sort(() => Math.random() - 0.5);
    
    for (const productName of shuffledProducts) {
      if (foundProducts.length >= 3) break; // Limit to 3 products
      
      try {
        const response = await client.productsApi.getProductsApiV1ProductsGet(
          1, // page
          12, // elements
          undefined, // price_min
          undefined, // price_max
          undefined, // productType
          'created_at', // sort
          productName // search
        );
        
        if (response.data.products && response.data.products.length > 0) {
          // Add first product that matches (avoid duplicates)
          const product = response.data.products.find(p => 
            !foundProducts.find(fp => fp.id === p.id)
          );
          if (product) {
            foundProducts.push(product);
          }
        }
      } catch (err) {
        console.error(`Failed to search for ${productName}:`, err);
      }
    }

    // If we haven't found 3 products yet, try a broader search
    if (foundProducts.length < 3) {
      try {
        const response = await client.productsApi.getProductsApiV1ProductsGet(
          1,
          50,
          undefined,
          undefined,
          undefined,
          'created_at',
          undefined
        );
        if (response.data.products) {
          // Filter products that might match our search terms
          const searchTerms = productsToSearch.map(term => term.toLowerCase());
          const matchingProducts = response.data.products.filter(product => {
            if (foundProducts.length >= 3) return false;
            if (foundProducts.find(p => p.id === product.id)) return false;
            const productNameLower = product.name.toLowerCase();
            const descLower = (product.description || '').toLowerCase();
            return searchTerms.some(term => 
              productNameLower.includes(term) || descLower.includes(term)
            );
          });
          foundProducts.push(...matchingProducts.slice(0, 3 - foundProducts.length));
        }
      } catch (err) {
        console.error('Failed to fetch products:', err);
        setError('Failed to load products');
      }
    }

    // Ensure we only have maximum 3 products
    setProducts(foundProducts.slice(0, 3));
    setLoading(false);
    setSearchingProducts(false);
  };

  const handleAddToCart = async (productId) => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    try {
      await client.buyerApi.addToCartApiV1BuyersCartPost({
        product_id: productId,
        quantity: 1
      });
      alert('Product added to cart!');
    } catch (err) {
      alert('Failed to add product to cart');
      console.error(err);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  if (!quizCompleted) {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    const selectedAnswer = answers[currentQuestion.id];

    return (
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Astrology Personal Quiz</h1>
            <p className="text-gray-600 mb-8">
              Discover your perfect crystal match based on your personal preferences!
            </p>

            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Question {currentQuestionIndex + 1} of {quizQuestions.length}
                </span>
                <span className="text-sm text-gray-500">
                  {Math.round(((currentQuestionIndex + 1) / quizQuestions.length) * 100)}% Complete
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentQuestionIndex + 1) / quizQuestions.length) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                {currentQuestion.question}
              </h2>
              <div className="space-y-3">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerSelect(currentQuestion.id, index)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      selectedAnswer === index
                        ? 'border-indigo-600 bg-indigo-50'
                        : 'border-gray-300 hover:border-indigo-300 hover:bg-gray-50'
                    }`}
                  >
                    <span className="font-medium text-gray-900">{option}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="flex justify-between">
              <button
                onClick={handlePreviousQuestion}
                disabled={currentQuestionIndex === 0}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                onClick={handleNextQuestion}
                disabled={selectedAnswer === undefined}
                className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {currentQuestionIndex === quizQuestions.length - 1 ? 'Finish Quiz' : 'Next'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Quiz Complete!</h1>
          <p className="text-gray-600 mb-4">
            Based on your answers, we've found some perfect crystal matches for you!
          </p>
          {searchingProducts && (
            <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-4">
              Finding your perfect crystal matches...
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {loading && products.length === 0 ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-lg">Loading products...</div>
          </div>
        ) : (
          <>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Recommended Products for You
            </h2>
            {products.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((product) => (
                  <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                    <div className="aspect-w-1 aspect-h-1 w-full overflow-hidden bg-gray-200">
                      {product.images && product.images.length > 0 ? (
                        <img
                          src={product.images[0]?.image_url}
                          alt={product.name}
                          className="h-48 w-full object-cover object-center"
                        />
                      ) : (
                        <div className="h-48 w-full bg-gray-300 flex items-center justify-center">
                          <span className="text-gray-500">No Image</span>
                        </div>
                      )}
                    </div>
                    <div className="p-4">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">{product.name}</h3>
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{product.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xl font-bold text-indigo-600">
                          {formatPrice(product.price)}
                        </span>
                        <span className="text-sm text-gray-500">
                          Stock: {product.stock_quantity}
                        </span>
                      </div>
                      <button
                        onClick={() => handleAddToCart(product.id)}
                        disabled={product.stock_quantity === 0}
                        className="mt-4 w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
                      >
                        {product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">
                  No products found. Try browsing our catalog!
                </p>
                <button
                  onClick={() => router.push('/catalog')}
                  className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                  Go to Catalog
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
