import { configureStore } from '@reduxjs/toolkit';
import imageReducer from './ImageSlice';

const store = configureStore({
  reducer: {
    image: imageReducer,
  },
});

export default store;
