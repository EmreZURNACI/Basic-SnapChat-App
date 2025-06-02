import { createSlice } from "@reduxjs/toolkit";

const imageSlice = createSlice({
  name: "image",
  initialState: {
    uri: null,
    effect: null,
  },
  reducers: {
    setImage: (state, action) => {
      state.uri = action.payload;
    },
    setEffect: (state, action) => {
      state.effect = action.payload;
    },
  },
});

export const { setImage, setEffect } = imageSlice.actions;
export default imageSlice.reducer;
