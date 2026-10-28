import { useEffect, useState } from "react";
import { Copy, Download, LoaderCircle } from "lucide-react";
import { draftConcepts, renderDesign, type Blank, type Concept, type Look } from "@/lib/studio.functions";
import { useStudio, type Design } from "@/lib/studio-store";

const SAMPLE = `Trend: "quiet luxury" và "office siren" đang lên trên TikTok tuần này.
Keyword Etsy đang bán: bookish girl, dark academia sticker, late night library.
Đối thủ dùng câu "I'd rather be reading" với serif đen trắng, giá khoảng $18.
Ghi chú: khách 18–28, thích câu ngắn, không muốn meme ồn. Màu mực đen, kem, đỏ đô.`;

const BLANKS: { id: Blank; label: string }[] = [
  { id: "tee", label: "Áo" },
  { id: "poster", label: "Poster" },
  { id: "sticker", label: "Sticker" },
  { id: "tote", label: "Tote" },
  { id: "mug", label: "Cốc" },
];

const LOOKS: { id: Look; label: string }[] = [
  { id: "type", label: "Chữ" },
  { id: "badge", label: "Huy hiệu" },
  { id: "illustration", label: "Minh họa" },
  { id: "line", label: "Nét" },
  { id: "retro", label: "Retro" },
];

function listingText(design: Pick<Design, "title" | "description" | "tags">) {
  return `Title: ${design.title}\n\n${design.description}\n\nTags: ${design.tags.join(", ")}`;
}

export function StudioApp() {
  const studio = useStudio();
  const [ready, setReady] = useState(false);
  const [reading, setReading] = useState(false);
  const [printingId, setPrintingId] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState("");

  useEffect(() => {
    let alive = true;
    void Promise.resolve(useStudio.persist.rehydrate()).finally(() => {
      if (alive) setReady(true);
    });
    return () => {
      alive = false;
    };
  }, []);

  async function onRead() {
    setError("");
    if (studio.notes.trim().length < 20) {
      setError("Dán thêm ghi chú — ít nhất một đoạn trend, keyword hoặc đối thủ.");
      return;
    }
    setReading(true);
    try {
      const result = await draftConcepts({
        data: {
          notes: studio.notes,
          blank: studio.blank,
          look: studio.look,
          sloganLang: studio.sloganLang,
        },
      });
      if (!result.ok) {
        setError(result.error);
        return;
      }
      studio.acceptDraft(result.read, result.concepts);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không đọc được ghi chú");
    } finally {
      setReading(false);
    }
  }

  async function onPrint(concept: Concept) {
    setError("");
    setPrintingId(concept.id);
    try {
      const prompt = studio.promptEdits[concept.id] ?? concept.imagePrompt;
      const result = await renderDesign({
        data: {
          slogan: concept.slogan,
          prompt,
          look: studio.look,
          blank: studio.blank,
        },
      });
      if (!result.ok) {
        setError(result.error);
        return;
      }
      studio.addDesign({
        id: crypto.randomUUID(),
        conceptId: concept.id,
        slogan: concept.slogan,
        imageUrl: result.url,
        title: concept.title,
        description: concept.description,
        tags: concept.tags,
        createdAt: Date.now(),
      });
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không in được ảnh");
    } finally {
      setPrintingId(null);
    }
  }

  async function onCopy(id: string, text: string) {
    await navigator.clipboard.writeText(text);
    setCopied(id);
    window.setTimeout(() => setCopied((current) => (current === id ? "" : current)), 1600);
  }

  async function onDownload(design: Design) {
    try {
      const res = await fetch(design.imageUrl);
      if (!res.ok) throw new Error("fetch failed");
      const blob = await res.blob();
      const href = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = href;
      link.download = `${design.slogan.slice(0, 40).replace(/\s+/g, "-").toLowerCase()}.png`;
      link.click();
      URL.revokeObjectURL(href);
    } catch {
      window.open(design.imageUrl, "_blank", "noopener,noreferrer");
    }
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-6 sm:px-6 sm:py-8">
      <header className="mb-6 flex items-end justify-between gap-4 border-b border-line pb-5">
        <div>
          <p className="mb-2 flex items-center gap-2 text-xs font-medium tracking-widest text-muted uppercase">
            <span className="inline-block size-2.5 bg-press" aria-hidden="true" />
            Seedline
          </p>
          <h1 className="text-3xl text-ink sm:text-4xl">Từ ghi chú trend ra file in.</h1>
        </div>
        <p className="hidden max-w-xs text-right text-sm text-muted sm:block">
          Ảnh phẳng và listing tiếng Anh. Bạn tải về rồi đưa lên Printify.
        </p>
      </header>

      <div className="grid items-start gap-6 lg:grid-cols-[20rem_1fr]">
        <section className="border border-line bg-sheet p-4 sm:p-5">
          <div className="mb-3 flex items-center justify-between gap-3">
            <h2 className="text-xl">Nguồn</h2>
            <button
              type="button"
              className="text-sm text-press underline-offset-2 hover:underline"
              onClick={() => studio.setNotes(SAMPLE)}
            >
              Điền mẫu
            </button>
          </div>
          <label className="sr-only" htmlFor="notes">
            Ghi chú trend
          </label>
          <textarea
            id="notes"
            value={ready ? studio.notes : ""}
            onChange={(event) => studio.setNotes(event.target.value)}
            placeholder="Dán keyword, hook TikTok, ghi chú đối thủ, màu, đối tượng khách…"
            rows={9}
            className="w-full resize-y border border-line bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted"
          />

          <fieldset className="mt-4">
            <legend className="mb-2 text-sm text-muted">Sản phẩm</legend>
            <div className="flex flex-wrap gap-2">
              {BLANKS.map((blank) => (
                <Chip
                  key={blank.id}
                  pressed={studio.blank === blank.id}
                  onClick={() => studio.setBlank(blank.id)}
                >
                  {blank.label}
                </Chip>
              ))}
            </div>
          </fieldset>

          <fieldset className="mt-4">
            <legend className="mb-2 text-sm text-muted">Kiểu hình</legend>
            <div className="flex flex-wrap gap-2">
              {LOOKS.map((look) => (
                <Chip key={look.id} pressed={studio.look === look.id} onClick={() => studio.setLook(look.id)}>
                  {look.label}
                </Chip>
              ))}
            </div>
          </fieldset>

          <fieldset className="mt-4">
            <legend className="mb-2 text-sm text-muted">Ngôn ngữ câu in</legend>
            <div className="flex gap-2">
              <Chip pressed={studio.sloganLang === "en"} onClick={() => studio.setSloganLang("en")}>
                English
              </Chip>
              <Chip pressed={studio.sloganLang === "vi"} onClick={() => studio.setSloganLang("vi")}>
                Tiếng Việt
              </Chip>
            </div>
          </fieldset>

          <button
            type="button"
            disabled={reading}
            onClick={() => void onRead()}
            className="mt-5 flex min-h-11 w-full items-center justify-center gap-2 bg-press px-4 text-sm font-medium text-sheet disabled:opacity-60"
          >
            {reading ? <LoaderCircle className="size-4 animate-spin" /> : null}
            {reading ? "Đang đọc ghi chú" : "Tách 4 concept"}
          </button>
          {error ? <p className="mt-3 text-sm text-press">{error}</p> : null}
        </section>

        <section className="flex flex-col gap-6">
          {studio.concepts.length === 0 ? (
            <Empty />
          ) : (
            <>
              {studio.read ? <p className="text-sm text-muted">{studio.read}</p> : null}
              <ul className="flex flex-col gap-4">
                {studio.concepts.map((concept, index) => (
                  <li key={concept.id} className="border border-line bg-sheet p-4 sm:p-5">
                    <p className="text-xs tracking-widest text-muted uppercase">Concept {index + 1}</p>
                    <h3 className="mt-1 text-2xl">{concept.slogan}</h3>
                    <p className="mt-2 text-sm text-ink">{concept.angle}</p>
                    <p className="mt-1 text-sm text-muted">{concept.visual}</p>
                    <label className="mt-4 block text-xs tracking-widest text-muted uppercase" htmlFor={`prompt-${concept.id}`}>
                      Prompt ảnh
                    </label>
                    <textarea
                      id={`prompt-${concept.id}`}
                      rows={3}
                      value={studio.promptEdits[concept.id] ?? concept.imagePrompt}
                      onChange={(event) => studio.setPrompt(concept.id, event.target.value)}
                      className="mt-1 w-full resize-y border border-line bg-paper px-3 py-2 text-sm"
                    />
                    <button
                      type="button"
                      disabled={printingId !== null}
                      onClick={() => void onPrint(concept)}
                      className="mt-3 flex min-h-11 items-center justify-center gap-2 bg-ink px-4 text-sm font-medium text-sheet disabled:opacity-60"
                    >
                      {printingId === concept.id ? <LoaderCircle className="size-4 animate-spin" /> : null}
                      {printingId === concept.id ? "Đang in" : "Tạo ảnh"}
                    </button>
                  </li>
                ))}
              </ul>
            </>
          )}

          {studio.designs.length > 0 ? (
            <div>
              <div className="mb-3 flex items-baseline justify-between gap-3">
                <h2 className="text-xl">Bản in</h2>
                <button
                  type="button"
                  className="text-sm text-muted underline-offset-2 hover:underline"
                  onClick={() => studio.clearDesigns()}
                >
                  Xóa bản đã lưu
                </button>
              </div>
              <p className="mb-3 text-sm text-muted">Tải ảnh ngay. Link có hạn, listing thì giữ trên máy này.</p>
              <ul className="grid gap-4 sm:grid-cols-2">
                {studio.designs.map((design) => (
                  <li key={design.id} className="border border-line bg-sheet">
                    <img
                      src={design.imageUrl}
                      alt={design.slogan}
                      className="aspect-square w-full bg-paper object-contain"
                    />
                    <div className="flex flex-col gap-3 p-4">
                      <h3 className="text-lg">{design.slogan}</h3>
                      <p className="text-sm text-ink">{design.title}</p>
                      <p className="text-sm text-muted">{design.description}</p>
                      <p className="text-xs text-muted">{design.tags.join(" · ")}</p>
                      <div className="flex flex-wrap gap-2">
                        <button
                          type="button"
                          onClick={() => void onCopy(design.id, listingText(design))}
                          className="inline-flex min-h-11 items-center gap-2 border border-line px-3 text-sm"
                        >
                          <Copy className="size-4" />
                          {copied === design.id ? "Đã chép" : "Chép listing"}
                        </button>
                        <button
                          type="button"
                          onClick={() => void onDownload(design)}
                          className="inline-flex min-h-11 items-center gap-2 border border-line px-3 text-sm"
                        >
                          <Download className="size-4" />
                          Tải ảnh
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </section>
      </div>
    </main>
  );
}

function Chip({
  pressed,
  onClick,
  children,
}: {
  pressed: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      type="button"
      aria-pressed={pressed}
      onClick={onClick}
      className={
        pressed
          ? "min-h-11 border border-ink bg-ink px-3 text-sm text-sheet"
          : "min-h-11 border border-line bg-paper px-3 text-sm text-ink"
      }
    >
      {children}
    </button>
  );
}

function Empty() {
  return (
    <div className="border border-dashed border-line bg-sheet px-5 py-10">
      <h2 className="text-2xl">Ba bước</h2>
      <ol className="mt-4 flex max-w-md flex-col gap-3 text-sm text-ink">
        <li>1. Dán trend, keyword, ghi chú đối thủ vào cột nguồn.</li>
        <li>2. Tách concept — mỗi concept là một câu in và một hướng hình.</li>
        <li>3. Tạo ảnh từng cái. File ra phẳng, kèm title, mô tả và tag để đưa lên Printify.</li>
      </ol>
    </div>
  );
}
