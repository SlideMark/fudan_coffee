/**
 * Created by irish on 16/9/14.
 */
!function(){function e(){var e=n.getBoundingClientRect().width,t=750,i=t/100;e>=750&&(e=750),n.style.fontSize=e/i+"px"}var t,n=document.documentElement,i=window.devicePixelRatio;n.setAttribute("data-dpr",i);var d=function(){clearTimeout(t),t=setTimeout(e,200)};window.addEventListener("resize",d,!1),window.addEventListener("pageshow",d,!1),window.addEventListener("orientationchange",d,!1),e()}();