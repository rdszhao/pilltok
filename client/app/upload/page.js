'use client'

import {Box, Button, Typography} from '@mui/material'
import {useState, useRef} from 'react'
import Image from 'next/image'

export default function Upload() {
  const fileInputRef = useRef(null)
  const [images, setImages] = useState([])

  const handleImageChange = (event) => {
    const files = Array.from(event.target.files)
    processFiles(files)
  }

  const processFiles = (files) => {
    const readers = []

    // Clear the previous images
    setImages([])

    files.forEach((file) => {
      const reader = new FileReader()
      readers.push(
        new Promise((resolve) => {
          reader.onload = (e) => {
            resolve(e.target.result)
          }
          reader.readAsDataURL(file)
        }),
      )
    })

    Promise.all(readers).then((encodedImages) => {
      setImages(encodedImages)
    })
  }

  const handleDrop = (event) => {
    event.preventDefault()
    event.stopPropagation()
    const files = Array.from(event.dataTransfer.files)
    processFiles(files)
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

  return (
    <Box
      width="100vw"
      height="100vh"
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      p={4}
    >
      <Box
        width="80%"
        height="70%"
        border="2px dashed gray"
        display="flex"
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        onClick={() => fileInputRef.current.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        sx={{
          cursor: 'pointer',
          '&:hover': {
            borderColor: 'primary.main',
          },
        }}
      >
        <Typography variant="button" textAlign="center">
          Click to upload or drag images here
        </Typography>
        <input
          type="file"
          accept="image/png, image/jpeg"
          onChange={handleImageChange}
          multiple
          ref={fileInputRef}
          hidden
        />
      </Box>
      <Box
        display="flex"
        flexWrap="wrap"
        gap={2}
        justifyContent="center"
        mt={4}
      >
        {images.map((src, index) => (
          <Box key={index} width={100} height={100} position="relative">
            <Image
              src={src}
              alt={`Uploaded image ${index}`}
              layout="fill"
              objectFit="cover"
            />
          </Box>
        ))}
      </Box>
    </Box>
  )
}
