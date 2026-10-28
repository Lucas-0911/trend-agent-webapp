import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

export const blanks = ["tee", "poster", "sticker", "tote", "mug"] as const;
export const looks = ["type", "badge", "illustration", "line", "retro"] as const;

export type Blank = (typeof blanks)[number];
export type Look = (typeof looks)[number];

export type Concept = {
  id: string;
  slogan: string;
  angle: string;
  visual: string;
  imagePrompt: string;
  title: string;
  description: string;
  tags: string[];
};

const blankLabel: Record<Blank, string> = {
  tee: "unisex t-shirt",
  poster: "art print poster",
  sticker: "die-cut sticker",
  tote: "canvas tote bag",
  mug: "ceramic mug",
};

const lookLabel: Record<Look, string> = {
  type: "typography-first poster where the slogan is the artwork",
  badge: "compact vintage badge or crest, emblem centered",
  illustration: "flat illustration, limited palette, no photorealism",
  line: "single-weight line art on a plain ground",
  retro: "retro screen-print, limited ink colors, slightly worn but clean",
};

const BriefInput = z.object({
  notes: z.string().trim().min(20).max(6000),
  blank: z.enum(blanks),
  look: z.enum(looks),
  sloganLang: z.enum(["vi", "en"]),
});

const ImageInput = z.object({
  slogan: z.string().trim().min(1).max(120),
  prompt: z.string().trim().min(8).max(2000),
  look: z.enum(looks),
  blank: z.enum(blanks),
});

const ConceptSchema = z.object({
  slogan: z.string().trim().min(1).max(120),
  angle: z.string().trim().min(1).max(400),
  visual: z.string().trim().min(1).max(500),
  imagePrompt: z.string().trim().min(8).max(2000),
  title: z.string().trim().min(1).max(160),
  description: z.string().trim().min(1).max(800),
  tags: z.array(z.string().trim().min(1).max(40)).min(3).max(13),
});

function extractJson(text: string): unknown {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  const raw = fenced?.[1] ?? text;
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start < 0 || end <= start) {
    throw new Error("Phản hồi không phải JSON");
  }
  return JSON.parse(raw.slice(start, end + 1));
}

async function chat(apiKey: string, user: string): Promise<string> {
  const res = await fetch("https://api.x.ai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: "grok-4.5",
      temperature: 0.7,
      max_tokens: 2200,
      response_format: { type: "json_object" },
      messages: [
        {
          role: "system",
          content:
            "You turn a print-on-demand seller's trend notes into design briefs. Reply with JSON only. Never invent sales numbers. Slogan language must match the request. Listing title, description and tags are English for Etsy. imagePrompt is English, describing flat artwork only — never a mockup, model, or photo of a product.",
        },
        { role: "user", content: user },
      ],
    }),
  });

  if (!res.ok) {
    const detail = (await res.text()).slice(0, 180);
    throw new Error(`Không đọc được trend (${res.status}). ${detail}`);
  }

  const body = (await res.json()) as {
    choices?: { message?: { content?: string } }[];
  };
  const text = body.choices?.[0]?.message?.content ?? "";
  if (!text) throw new Error("Trend không trả về nội dung");
  return text;
}

function aspectFor(blank: Blank): "1:1" | "3:4" {
  return blank === "poster" ? "3:4" : "1:1";
}

function printPrompt(slogan: string, prompt: string, look: Look): string {
  const textRule =
    look === "illustration"
      ? `If any lettering appears, it is only this exact phrase and nothing else: "${slogan}". Prefer the illustration carrying the idea, with the phrase small or omitted if it crowds the art.`
      : `Render this exact phrase as the only text, spelled correctly, no extra words, no watermark: "${slogan}".`;

  return [
    prompt,
    textRule,
    "Flat print-ready artwork file on a plain background. Not a photograph of a shirt, mug, poster on a wall, person, shop, or packaging mockup.",
    "Centered, generous quiet margin, high contrast, crisp edges, no signature, no UI.",
  ].join(" ");
}

export const draftConcepts = createServerFn({ method: "POST" })
  .validator((input: unknown) => BriefInput.parse(input))
  .handler(async ({ data }) => {
    const apiKey = process.env.XAI_API_KEY;
    if (!apiKey) {
      return { ok: false as const, error: "Tạo ảnh bằng AI chưa bật trong môi trường này." };
    }

    const lang = data.sloganLang === "vi" ? "Vietnamese" : "English";
    const ask = `Seller notes:\n${data.notes}\n\nProduct: ${blankLabel[data.blank]}\nLook: ${lookLabel[data.look]}\nSlogan language: ${lang}\n\nReturn JSON:\n{"read":"one Vietnamese sentence on what you took from the notes","concepts":[{"slogan":"","angle":"one Vietnamese sentence why this fits","visual":"one Vietnamese sentence of what the art looks like","imagePrompt":"dense English prompt for the flat artwork","title":"Etsy title under 140 characters mentioning the product","description":"two English sentences a buyer would read","tags":["exactly 13 short English tags"]}]}\nExactly 4 concepts. Slogans max 8 words. Do not repeat the same joke.`;

    try {
      const text = await chat(apiKey, ask);
      const parsed = z
        .object({
          read: z.string().trim().min(1).max(400),
          concepts: z.array(ConceptSchema).min(1).max(6),
        })
        .parse(extractJson(text));

      const concepts: Concept[] = parsed.concepts.slice(0, 4).map((concept) => ({
        ...concept,
        id: crypto.randomUUID(),
        tags: concept.tags.slice(0, 13),
      }));

      return { ok: true as const, read: parsed.read, concepts };
    } catch (error) {
      const message = error instanceof Error ? error.message : "Không tách được concept";
      return { ok: false as const, error: message };
    }
  });

export const renderDesign = createServerFn({ method: "POST" })
  .validator((input: unknown) => ImageInput.parse(input))
  .handler(async ({ data }) => {
    const apiKey = process.env.XAI_API_KEY;
    if (!apiKey) {
      return { ok: false as const, error: "Tạo ảnh bằng AI chưa bật trong môi trường này." };
    }

    const prompt = printPrompt(data.slogan, data.prompt, data.look);
    const models = ["grok-imagine-image", "grok-imagine-image-2.0"];
    let last = "Không tạo được ảnh";

    for (const model of models) {
      const res = await fetch("https://api.x.ai/v1/images/generations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          prompt,
          n: 1,
          aspect_ratio: aspectFor(data.blank),
          resolution: "1k",
          response_format: "url",
        }),
      });

      if (!res.ok) {
        last = `Ảnh lỗi ${res.status}`;
        if (res.status !== 400 && res.status !== 404) break;
        continue;
      }

      const body = (await res.json()) as {
        data?: { url?: string }[];
      };
      const url = body.data?.[0]?.url;
      if (!url) {
        last = "Ảnh không có đường dẫn";
        continue;
      }
      return { ok: true as const, url };
    }

    return { ok: false as const, error: last };
  });
