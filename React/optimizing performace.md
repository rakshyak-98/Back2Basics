**A functional component will render for one of three reasons:**
- Then component was not in the component tree before and is now.
- The parent component just re-rendered.
- The component uses a hook that has flagged this component for re-render.

> [!NOTE] React might batch rendering after several of these things happen.

if a state value changes and the parent component re-renders, for example, the component might re-render once, or it might re-render twice.