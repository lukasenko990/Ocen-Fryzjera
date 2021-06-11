function expand()
{
    var elements=document.getElementsByClassName("hidden");
    var i;
    for(i=0; i<elements.length; i++)
    {
        elements[i].style.display="inline";
    }
    document.getElementById('expandUtility').innerHTML="Zwiń&nbsp;listę&nbsp;opinii"
    document.getElementById('expandUtility').href="javascript:collapse()"
}

function collapse()
{
    var elements=document.getElementsByClassName("hidden");
    var i;
    for(i=0; i<elements.length; i++)
    {
        elements[i].style.display="none";
    }
    document.getElementById('expandUtility').innerHTML="Pokaż&nbsp;więcej"
    document.getElementById('expandUtility').href="javascript:expand()"
}
