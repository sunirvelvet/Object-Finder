import React, { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

const ObjectFinder = () => {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5001/find_object', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Network response was not ok');
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setImage({ imageUrl });
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
      setImage(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Object Finder</h1>
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex gap-2">
          <Input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter object to find..."
            className="flex-grow"
          />
          <Button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Find Object'}
          </Button>
        </div>
      </form>
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      {image && (
        <Card className="p-4">
          <div className="relative">
            <img src={image.imageUrl} alt="Result" className="w-full h-auto" />
          </div>
        </Card>
      )}
    </div>
  );
};

export default ObjectFinder;
