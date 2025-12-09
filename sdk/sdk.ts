import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
    ProductsApi,
    BuyersApi,
    SellersApi,
    SuppliersApi,
    AuthenticationApi,
} from './api';
import { Configuration } from './configuration';
  
export class ApiSDK {
    private authApi: AuthenticationApi;
    private productsApi: ProductsApi;
    private buyerApi: BuyersApi;
    private sellerApi: SellersApi;
    private supplierApi: SuppliersApi;
    private token: string | null = null;
    private axiosInstance: AxiosInstance;
  
    constructor(basePath?: string) {
        this.axiosInstance = axios.create({ 
          baseURL: basePath,
          withCredentials: true
        });
        this.setupInterceptors();
        const config = new Configuration({
          basePath,
          apiKey: () => this.getAuthHeader(),
          baseOptions: { 
            axios: this.axiosInstance
          },
        });
        
        this.authApi = new AuthenticationApi(config, undefined, this.axiosInstance);
        this.productsApi = new ProductsApi(config, undefined, this.axiosInstance);
        this.buyerApi = new BuyersApi(config, undefined, this.axiosInstance);
        this.sellerApi = new SellersApi(config, undefined, this.axiosInstance);
        this.supplierApi = new SuppliersApi(config, undefined, this.axiosInstance);
      }
  
    public setToken(newToken: string) {
      this.token = newToken;
    }
    private getAuthHeader(): string {
      if (!this.token) {
        throw new Error('No token set. Call setToken() first.');
      }
      return `Bearer ${this.token}`;
    }
  
    private setupInterceptors() {
    this.axiosInstance.interceptors.request.use((config) => {
        if (this.token) {
        config.headers['Authorization'] = this.getAuthHeader();
        }
        return config;
    });
    
    this.axiosInstance.interceptors.response.use((response: AxiosResponse) => {
        const newToken = response.data.newToken || response.headers['Authorization'];
        if (newToken) {
        this.setToken(newToken.replace('Bearer ', ''));
        console.log('Token automatically updated via backend refresh');
        }
        return response;
    }, (error) => {
        if (error.response?.status === 401) {
        console.error('Authentication failed - session expired');
        }
        return Promise.reject(error);
    });
    }
    public getApi() {
      return {
        authApi: this.authApi,
        productsApi: this.productsApi,
        buyerApi: this.buyerApi,
        sellerApi: this.sellerApi,
        supplierApi: this.supplierApi,
      };
    }
  }