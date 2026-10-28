import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Blank, Concept, Look } from "@/lib/studio.functions";

export type Design = {
  id: string;
  conceptId: string;
  slogan: string;
  imageUrl: string;
  title: string;
  description: string;
  tags: string[];
  createdAt: number;
};

type Studio = {
  notes: string;
  blank: Blank;
  look: Look;
  sloganLang: "vi" | "en";
  read: string;
  concepts: Concept[];
  promptEdits: Record<string, string>;
  designs: Design[];
  setNotes: (notes: string) => void;
  setBlank: (blank: Blank) => void;
  setLook: (look: Look) => void;
  setSloganLang: (sloganLang: "vi" | "en") => void;
  setPrompt: (id: string, prompt: string) => void;
  acceptDraft: (read: string, concepts: Concept[]) => void;
  addDesign: (design: Design) => void;
  clearDesigns: () => void;
};

export const useStudio = create<Studio>()(
  persist(
    (set) => ({
      notes: "",
      blank: "tee",
      look: "type",
      sloganLang: "en",
      read: "",
      concepts: [],
      promptEdits: {},
      designs: [],
      setNotes: (notes) => set({ notes }),
      setBlank: (blank) => set({ blank }),
      setLook: (look) => set({ look }),
      setSloganLang: (sloganLang) => set({ sloganLang }),
      setPrompt: (id, prompt) =>
        set((state) => ({ promptEdits: { ...state.promptEdits, [id]: prompt } })),
      acceptDraft: (read, concepts) =>
        set({
          read,
          concepts,
          promptEdits: Object.fromEntries(concepts.map((concept) => [concept.id, concept.imagePrompt])),
        }),
      addDesign: (design) => set((state) => ({ designs: [design, ...state.designs].slice(0, 24) })),
      clearDesigns: () => set({ designs: [] }),
    }),
    { name: "seedline", skipHydration: true },
  ),
);
