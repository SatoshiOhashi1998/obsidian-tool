import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

export default function ObsiTool() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('title');
  const [results, setResults] = useState([]);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);

  const pageSize = 10; // APIの1ページあたり件数に合わせて調整してください
  const totalPages = Math.ceil(totalCount / pageSize);

  // タイマーIDを保持
  const debounceTimeout = useRef(null);

  // APIからデータ取得
  const fetchResults = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/notes/search/', {
        params: { q: query, mode, page },
      });
      setResults(res.data.results || res.data);
      setTotalCount(res.data.count || res.data.length);
    } catch (e) {
      console.error('API取得エラー', e);
    }
    setLoading(false);
  };

  // 検索ボタン押下
  const onSearch = e => {
    e.preventDefault();
    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);
    setPage(1);
    fetchResults();
  };

  // query または mode が変わったら500ms後にfetch
  useEffect(() => {
    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);

    debounceTimeout.current = setTimeout(() => {
      setPage(1); // 入力・モード変更時はページ1にリセット
      fetchResults();
    }, 15000000);

    return () => clearTimeout(debounceTimeout.current);
  }, [query, mode]);

  // pageが変わったら即fetch
  useEffect(() => {
    fetchResults();
  }, [page]);

  // ダウンロード処理
  const forceDownload = (url, filename) => {
    fetch(url)
      .then(resp => resp.blob())
      .then(blob => {
        const blobUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = filename || 'download';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(blobUrl);
      })
      .catch(() => alert('ダウンロードに失敗しました'));
  };

  const buttonStyle = {
    margin: '0 4px',
    padding: '6px 12px',
    border: '1px solid #2980b9',
    borderRadius: 4,
    cursor: 'pointer',
    backgroundColor: 'white',
    color: '#2980b9',
  };

  return (
    <div
      style={{
        maxWidth: 960,
        margin: '20px auto',
        fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif',
        backgroundColor: '#f7f9fc',
        color: '#333',
        lineHeight: 1.5,
        padding: '0 15px',
      }}
    >
      <h1
        style={{
          textAlign: 'center',
          marginBottom: 30,
          color: '#2c3e50',
        }}
      >
        画像検索
      </h1>

      <form
        onSubmit={onSearch}
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: 15,
          marginBottom: 30,
        }}
      >
        <input
          type="text"
          placeholder="検索ワード"
          value={query}
          onChange={e => setQuery(e.target.value)}
          style={{
            flex: '1 1 300px',
            padding: '10px 12px',
            fontSize: 16,
            border: '2px solid #ccc',
            borderRadius: 6,
            transition: 'border-color 0.3s ease',
          }}
          onFocus={e => (e.target.style.borderColor = '#2980b9')}
          onBlur={e => (e.target.style.borderColor = '#ccc')}
        />

        <label
          style={{
            fontSize: 15,
            color: '#555',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            cursor: 'pointer',
          }}
        >
          <input
            type="radio"
            name="mode"
            value="title"
            checked={mode === 'title'}
            onChange={() => setMode('title')}
            style={{ cursor: 'pointer' }}
          />
          タイトルで検索
        </label>

        <label
          style={{
            fontSize: 15,
            color: '#555',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            cursor: 'pointer',
          }}
        >
          <input
            type="radio"
            name="mode"
            value="tag"
            checked={mode === 'tag'}
            onChange={() => setMode('tag')}
            style={{ cursor: 'pointer' }}
          />
          タグで検索
        </label>

        <button
          type="submit"
          style={{
            backgroundColor: '#2980b9',
            color: 'white',
            padding: '10px 20px',
            fontSize: 16,
            border: 'none',
            borderRadius: 6,
            cursor: 'pointer',
            boxShadow: '0 3px 8px rgba(41,128,185,0.4)',
            transition: 'background-color 0.3s ease',
          }}
          onMouseOver={e => (e.currentTarget.style.backgroundColor = '#1c5d8a')}
          onMouseOut={e => (e.currentTarget.style.backgroundColor = '#2980b9')}
        >
          検索
        </button>
      </form>

      <hr style={{ border: 'none', borderTop: '1px solid #ddd', margin: '30px 0' }} />

      {loading ? (
        <p style={{ textAlign: 'center' }}>読み込み中...</p>
      ) : results.length === 0 ? (
        <p
          className="no-results"
          style={{ fontSize: 16, textAlign: 'center', color: '#999', marginTop: 40 }}
        >
          {query ? '該当する画像はありません。' : '検索してください。'}
        </p>
      ) : (
        <>
          <h2
            style={{
              marginBottom: 20,
              color: '#34495e',
              borderBottom: '2px solid #2980b9',
              paddingBottom: 6,
              fontWeight: 600,
            }}
          >
            画像一覧（{results.length}件）
          </h2>

          {results.map(note => (
            <div key={note.id} style={{ marginBottom: 40 }}>
              <p style={{ fontWeight: 600, marginBottom: 12, color: '#2c3e50', fontSize: 16 }}>
                {note.filename}
              </p>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
                  gap: 16,
                }}
              >
                {(note.image_urls || []).map((img_url, i) => (
                  <div
                    key={i}
                    style={{
                      textAlign: 'center',
                      backgroundColor: 'white',
                      borderRadius: 10,
                      boxShadow: '0 3px 10px rgba(0,0,0,0.08)',
                      padding: '12px 8px 16px',
                      transition: 'box-shadow 0.3s ease',
                    }}
                    onMouseEnter={e =>
                      (e.currentTarget.style.boxShadow = '0 8px 18px rgba(0,0,0,0.18)')
                    }
                    onMouseLeave={e =>
                      (e.currentTarget.style.boxShadow = '0 3px 10px rgba(0,0,0,0.08)')
                    }
                  >
                    <img
                      src={img_url}
                      alt="画像"
                      style={{
                        maxWidth: '100%',
                        maxHeight: 180,
                        borderRadius: 8,
                        objectFit: 'cover',
                        marginBottom: 10,
                        cursor: 'pointer',
                        transition: 'transform 0.3s ease',
                      }}
                      onMouseOver={e => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 6px 14px rgba(0,0,0,0.25)';
                      }}
                      onMouseOut={e => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}
                    />
                    <button
                      type="button"
                      className="download-btn"
                      onClick={() => forceDownload(img_url, img_url.slice(-20))}
                      style={{
                        display: 'inline-block',
                        padding: '7px 18px',
                        fontSize: 14,
                        backgroundColor: '#2980b9',
                        color: 'white',
                        borderRadius: 6,
                        textDecoration: 'none',
                        boxShadow: '0 3px 7px rgba(41, 128, 185, 0.5)',
                        border: 'none',
                        cursor: 'pointer',
                        transition: 'background-color 0.3s ease',
                      }}
                      onMouseOver={e => (e.currentTarget.style.backgroundColor = '#1c5d8a')}
                      onMouseOut={e => (e.currentTarget.style.backgroundColor = '#2980b9')}
                    >
                      ダウンロード
                    </button>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* ページネーション */}
          <nav style={{ marginTop: 30, textAlign: 'center' }}>
            <button
              onClick={() => setPage(1)}
              disabled={page === 1}
              style={{
                ...buttonStyle,
                cursor: page === 1 ? 'default' : 'pointer',
                color: page === 1 ? '#ccc' : '#2980b9',
                borderColor: page === 1 ? '#ccc' : '#2980b9',
              }}
            >
              最初へ
            </button>

            <button
              onClick={() => setPage(p => Math.max(p - 1, 1))}
              disabled={page === 1}
              style={{
                ...buttonStyle,
                cursor: page === 1 ? 'default' : 'pointer',
                color: page === 1 ? '#ccc' : '#2980b9',
                borderColor: page === 1 ? '#ccc' : '#2980b9',
              }}
            >
              &lt; 前へ
            </button>

            {[...Array(totalPages)].map((_, i) => {
              const pageNum = i + 1;
              return (
                <button
                  key={pageNum}
                  onClick={() => setPage(pageNum)}
                  disabled={page === pageNum}
                  style={{
                    ...buttonStyle,
                    fontWeight: page === pageNum ? 'bold' : 'normal',
                    backgroundColor: page === pageNum ? '#2980b9' : 'white',
                    color: page === pageNum ? 'white' : '#2980b9',
                    cursor: page === pageNum ? 'default' : 'pointer',
                  }}
                >
                  {pageNum}
                </button>
              );
            })}

            <button
              onClick={() => setPage(p => Math.min(p + 1, totalPages))}
              disabled={page === totalPages}
              style={{
                ...buttonStyle,
                cursor: page === totalPages ? 'default' : 'pointer',
                color: page === totalPages ? '#ccc' : '#2980b9',
                borderColor: page === totalPages ? '#ccc' : '#2980b9',
              }}
            >
              次へ &gt;
            </button>

            <button
              onClick={() => setPage(totalPages)}
              disabled={page === totalPages}
              style={{
                ...buttonStyle,
                cursor: page === totalPages ? 'default' : 'pointer',
                color: page === totalPages ? '#ccc' : '#2980b9',
                borderColor: page === totalPages ? '#ccc' : '#2980b9',
              }}
            >
              最後へ
            </button>
          </nav>
        </>
      )}
    </div>
  );
}
