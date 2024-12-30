'use client';

import {useEffect, useState} from "react";

import {Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious} from "@/components/ui/carousel";

import Autoplay from "embla-carousel-autoplay";
import Fade from "embla-carousel-fade";

interface Image {
    id: number
    url: string
    alt: string
}


export function ImageCarousel() {
    const [images, setImages] = useState<Image[]>([
        {
            id: 1,
            url: 'https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
            alt: 'image-1'
        },
        {
            id: 2,
            url: 'https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
            alt: 'image-2'
        },
        {
            id: 3,
            url: 'https://images.pexels.com/photos/777001/pexels-photo-777001.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
            alt: 'image-3'
        },
        {
            id: 4,
            url: 'https://images.pexels.com/photos/1029757/pexels-photo-1029757.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
            alt: 'image-4',
        }
    ]);
    const [api, setApi] = useState<any>();
    const [current, setCurrent] = useState(0);
    const [delay, setDelay] = useState(4000);

    useEffect(() => {
    }, []);

    useEffect(() => {
        if (!api) return;

        setCurrent(api.selectedScrollSnap());

        const onSelect = () => setCurrent(api.selectedScrollSnap());

        api.on("select", onSelect);

        return () => {
            api.off("select", onSelect);
        };
    }, [api]);

    const plugins: object = {delay: delay, stopOnInteraction: false, stopOnMouseEnter: true,};

    return (
        <div className="container mx-auto pt-5">
            <Carousel className="w-full" setApi={setApi} plugins={[Autoplay(plugins), Fade()]} opts={{loop: true}}>
                <CarouselContent>
                    {images.map((image) => (
                        <CarouselItem key={image.id}>
                            <div className={'relative w-full'}>
                                <img
                                    src={image.url}
                                    alt={image.alt}
                                    className="w-full h-[400px] md:h-[650px] object-cover rounded-lg"
                                />
                            </div>
                        </CarouselItem>
                    ))}
                </CarouselContent>
                <CarouselPrevious className="left-4"/>
                <CarouselNext className="right-4"/>
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
                    {images.map((_, index) => (
                        <button
                            key={index}
                            onClick={() => api?.scrollTo(index)}
                            className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${
                                current === index
                                    ? 'bg-white scale-110'
                                    : 'bg-white/50 hover:bg-white/75'
                            }`}
                            aria-label={`Go to slide ${index + 1}`}
                        />
                    ))}
                </div>
            </Carousel>
        </div>
    );
}